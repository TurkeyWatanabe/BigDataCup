import streamlit as st
import os
from utils import is_valid_team_id
from sqlalchemy import create_engine, text
import pandas as pd

st.write(r'''<style>
    
    [data-testid="baseButton-header"] {
        display:none !important;
         
    }
    [data-testid="stSidebarContent"] {
        background-color: #1E1C63 !important;
        color: white !important;
    }
    [data-testid="stSidebarContent"] span{
        color: white !important;
        font-size: calc(1rem * 1.2) !important;
    }

    </style>
         
         ''', unsafe_allow_html=True)

# 输入你的 GitHub 访问 token 和目标仓库信息
GITHUB_TOKEN = "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"
GITHUB_REPO = "TurkeyWatanabe/BigDataCup"
GITHUB_BRANCH = "main"

def upload_file_to_github(file, path_in_repo):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path_in_repo}"
    
    # 将文件编码为 base64 格式
    content = base64.b64encode(file.read()).decode("utf-8")
    
    # 构造请求头和请求体
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": f"Add {path_in_repo}",
        "content": content,
        "branch": GITHUB_BRANCH
    }
    
    # 发送 POST 请求到 GitHub API
    response = requests.put(url, json=data, headers=headers)
    
    # 检查请求结果
    if response.status_code == 201:
        st.success(f"File '{path_in_repo}' uploaded successfully to GitHub.")
    else:
        st.error(f"Failed to upload file to GitHub. Error: {response.json()}")

st.markdown("<center style='font-size:1.5rem'><b>IEEE Big Data 2024</b></center>", unsafe_allow_html=True)
st.markdown("<center>Washington DC, USA</center>", unsafe_allow_html=True)

st.markdown("### <span style='color:#1E1C63'>Challenges of Trustworthy AI in Distribution Shifts and Algorithmic Fairness 2024</span>", unsafe_allow_html=True)

st.markdown("#### Submission Rules")

st.markdown("The submission will be divided into three stages, with specific timing detailed in the <a href='http://192.168.1.112:8501/Important_Dates' target='_self'>Important Dates</a>. Each team is allowed unlimited submissions in each stage. The final result for each stage will be based on the team's last submission, and interim results for each stage will be announced on <a href='http://192.168.1.112:8501/Leaderboard' target='_self'>Leaderboard</a> within one week after the deadline. The team's final score will be based on the results of the third stage."
            , unsafe_allow_html=True)

st.markdown("""
            Each submission should be a `.zip` file named **only** by the team id (such as `Ix9oW1.zip`), which contains two folders, one for the runnable source code of task1 and the other for task2 (if necessary, include `requirement.txt`), and both should include a function `evaluation` for testing with the following input and output formats:
            + Input: 10000 three channel facial images of different sizes from Sketch domain.
            + Output: The metric result obtained from trained classifiers (Accuracy for task 1; Accuracy and $\Delta{DP}$ for task 2).

            At the end of each stage, we will test the team's last submission on our **test set** and publish the results on <a href='http://192.168.1.112:8501/Leaderboard' target='_self'>Leaderboard</a> within a week.
            
            **Note:** incorrectly named files will not be received!!!
            """
            , unsafe_allow_html=True)

st.markdown("#### Submission channel")

stage = 1
st.warning(f"Currently in the stage {stage} of submission")
st.info(f"Each submission should be a `.zip` file named **only** by the team id (such as `Ix9oW1.zip`)")
uploaded_file = st.file_uploader("Submit a `.zip` file named only after the team ID.", type="zip")
if st.button("Submit"):
    if uploaded_file is not None:
        # 检查命名格式
        if uploaded_file.name.endswith(".zip"):
            team_id = uploaded_file.name[:-4]
            # 检查是不是合法的team id格式
            if is_valid_team_id(team_id):
                # 检查team id是否存在
                # conn = st.connection('bigdatacupdb', type='sql')
                engine = create_engine('sqlite:////mount/src/bigdatacup/bigdatacup.db')
                with engine.connect() as connection:
                    # team_id_df = conn.query(f"select team_id from teamsForCup;",ttl=2)
                    team_id_df = connection.execute(text(f"select team_id from teamsForCup;"))
                    team_id_df = pd.DataFrame(team_id_df.fetchall(), columns=team_id_df.keys())
                
                team_id_list = team_id_df['team_id'].to_list()
                st.success(team_id_list)
                if team_id in team_id_list:
                    # with open(os.path.join(f"uploads/stage{stage}", uploaded_file.name), "wb") as f:
                    #     f.write(uploaded_file.getbuffer())
                    if uploaded_file is not None:
                        # 指定文件上传到仓库的路径
                        path_in_repo = f"uploads/stage{stage}/{uploaded_file.name}"  # 例如上传到 'uploads' 目录下
                        
                        # 上传文件到 GitHub
                        upload_file_to_github(uploaded_file, path_in_repo)
                    st.success(f'Team {team_id} submitted successfully!', icon="✅")
                else:
                    st.error(f'Team {team_id} not registered, please register first.', icon="🚨")
            else:
                st.error('Please check the naming format, it can only be team ID.', icon="🚨")
        else:
            st.error('Please upload a .zip file.', icon="🚨")
    else:
        st.error('Please upload a file first.', icon="🚨")
    
