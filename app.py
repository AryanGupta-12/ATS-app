from flask import Flask, request, render_template, jsonify, Response
import os
import fitz
from PIL import Image
import pytesseract
import shutil
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv(dotenv_path="config.env")
app = Flask(__name__)
app.config['RESUME_UPLOAD_FOLDER'] = 'uploads/resume/'
app.config['JD_UPLOAD_FOLDER'] = 'uploads/desc/'
app.config["RESUME_IMAGE_FOLDER"] = 'images/resumes/'
app.config['JD_IMAGE_FOLDER']= 'images/descriptions/'

os.makedirs(app.config['RESUME_UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['JD_UPLOAD_FOLDER'], exist_ok=True)

nlp = spacy.load('en_core_web_sm')

llm = ChatGroq(model="mixtral-8x7b-32768",temperature=0)

def clear_upload_folders():
    for file in [app.config['RESUME_UPLOAD_FOLDER'], app.config['JD_UPLOAD_FOLDER'],app.config["RESUME_IMAGE_FOLDER"], app.config['JD_IMAGE_FOLDER']]:
        if os.path.exists(file):
            shutil.rmtree(file)
        os.makedirs(file)


def preprocess(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)

def calculate_match_percentage(doc1, doc2):
    doc1 = preprocess(doc1)
    doc2 = preprocess(doc2)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([doc1,doc2])
    print(vectors.shape)
    print(vectors[0].shape)
    print(vectors[1].shape)
    cosine_sim = cosine_similarity(vectors[0],vectors[1])
    return round(cosine_sim[0][0],6)

def relevant_text_res(raw_dict, fields):
    rel_dict = {}
    count = 1
    for path,text in raw_dict.items():
        file_name = os.path.basename(path).split('.')[0]
        result=""
        system = "You are a helpful assistant which takes in input a resume and retrieve the required fields from it. Take everything from the context. dont make things on your own."
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
        chain = prompt | llm
        ans = chain.invoke({"text":f"Resume:{text}\nRequired fields are:{fields}"})
        result+=f"Start of Resume {count}:\n"
        result += ans.content
        result+=f"End of Resume {count}:\n\n"
        rel_dict[file_name]=(result)
        count+=1
    return rel_dict

def relevant_text_desc(raw_text, fields):
    rel_text = ''
    system = "You are a helpful assistant which takes in input a job description and retrieve the required fields from it. Take everything from the context. dont make things on your own."
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | llm
    ans = chain.invoke({"text":f"Job description:{raw_text}\nRequired fields are:{fields}"})
    rel_text+=ans.content
    return rel_text

def matching(resume, job_desc):
    system = "You are helpful assistant which matches a list of resumes and a job description given to you and tells which of the given resume matches the best to the job description and why (give details). Give only important details. Also give the match percentage for every resume.Take everything from the context. Dont make things on your own."
    human = "{text}"
    res_count = len(resume)
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | llm
    ans = chain.invoke({"text":f"Job description:{job_desc}\nThere are total {res_count} resumes.\nResume list:{resume}"})
    return ans.content

def pdf_to_images(pdf_path, type):
    pdf_document = fitz.open(pdf_path)
    if type == 'resume':
        count = 1
        dir = os.path.join(os.getcwd(),"images/resumes")
        while True:
                folder_name = f"resume{count}"
                if not os.path.exists(os.path.join(dir,folder_name)):
                    os.mkdir(os.path.join(dir,folder_name))
                    break
                else: count+=1
        paths = []
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            output_folder = os.path.join(dir,folder_name)
            image_path = f"{output_folder}\page_{page_num + 1}.png"
            image.save(image_path)
            paths.append(f"{image_path}")
    elif type == "desc":
        count = 1
        dir = os.path.join(os.getcwd(),"images/descriptions")
        while True:
                folder_name = f"desc{count}"
                if not os.path.exists(os.path.join(dir,folder_name)):
                    os.mkdir(os.path.join(dir,folder_name))
                    break
                else: count+=1
        paths = []
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            output_folder = os.path.join(dir,folder_name)
            image_path = f"{output_folder}\page_{page_num + 1}.png"
            image.save(image_path)
            paths.append(f"{image_path}")
        
    return paths

def extract_text_from_pdf(pdf_path, type):
    paths = pdf_to_images(pdf_path,type)
    full_text = ""
    for path in paths :    
        image = Image.open(path)
        image = image.convert("L")
        full_text += pytesseract.image_to_string(image)
        full_text+="\n"
    return full_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' in request.files:
        resume_files = request.files.getlist('resume')
        for resume in resume_files:
            resume.save(os.path.join(app.config['RESUME_UPLOAD_FOLDER'], resume.filename))
    return jsonify(message="Resumes uploaded successfully")

@app.route('/upload_jd', methods=['POST'])
def upload_jd():
    if 'job_description' in request.files:
        job_description = request.files['job_description']
        job_description.save(os.path.join(app.config['JD_UPLOAD_FOLDER'], job_description.filename))
    return jsonify(message="Job description uploaded successfully")

@app.route('/check_files', methods=['POST'])
def check_files():
    resume_files = os.listdir(app.config['RESUME_UPLOAD_FOLDER'])
    jd_files = os.listdir(app.config['JD_UPLOAD_FOLDER'])
    
    if not resume_files:
        return jsonify(message="No resumes uploaded. Please upload resumes before processing.")
    
    if not jd_files:
        return jsonify(message="No job description uploaded. Please upload a job description before processing.")
    return jsonify(message="Files are uploaded. Processing will start now.")

@app.route('/process', methods=['POST'])
def process():
    res_dict = {}
    desc_text = ""
    for file_path in os.listdir(app.config['RESUME_UPLOAD_FOLDER']):
        res_dict[file_path]=(extract_text_from_pdf("uploads/resume/"+file_path,type="resume"))
    
    desc_text+=extract_text_from_pdf("uploads/desc/"+(os.listdir(app.config['JD_UPLOAD_FOLDER'])[0]), type = "desc")
    relevant_text_resume = relevant_text_res(res_dict, fields=["Skills", "Experience", "Project"])
    relevant_desc = relevant_text_desc(desc_text,fields= ["Required Skills", "Required Qualifications"])
    result = matching(relevant_text_resume, relevant_desc)
    result+="\n\nCosine Similarity scores:\n"
    count = 1
    for file_path,res in res_dict.items():
        percent =( calculate_match_percentage(res,desc_text))*100
        result+=f"Resume {count}: {percent}%\n"
        count+=1
    clear_upload_folders()
    return Response(result, content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
