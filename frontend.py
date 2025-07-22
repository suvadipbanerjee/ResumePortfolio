import streamlit as st
import requests

st.markdown("<h1 style='text-align: center;'>SB RESUME TO PORTFOLIO MAKER</h1>", unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")

Templates,sec2=st.columns(2)

with Templates:
    L1=[]
    st.subheader("Select Your Template")
    options={
        "Template1":"https://themes.3rdwavemedia.com/wp-content/uploads/2019/04/bootstrap-portfolio-theme-for-developers-devcard.png",
        "Template2":"https://mir-s3-cdn-cf.behance.net/projects/404/b16be4226085281.Y3JvcCwxOTg4LDE1NTUsNCww.jpg"
    }
    L=list(options.keys())
    for i in range(0,2):
        st.image(options[L[i]])
        a=st.checkbox(label=L[i],key= str(i))
        if a :
            L1.append(L[i])




with sec2:
    st.subheader("Upload Your Resume in pdf")    

    updated_file = st.file_uploader("Select Your File ")
    if updated_file is not None:
        d={
            "file":(updated_file.name,updated_file,updated_file.type)
        }

        col1,col2,col3=st.columns(3)
        with col3:
            c=st.button("Proceed")

        if c:
            response=requests.post("http://localhost:8000/resumeP/"+L1[0],files= d)

            if response.status_code == 200:
                st.success("File sent successfully!")
                st.write(response.text)  
            else:
                st.error(f"Failed to send file. Status code: {response.status_code}")



            
    
