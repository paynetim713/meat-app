import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 页面基础配置 ---
st.set_page_config(page_title="识肉君 (云端版)", page_icon="🥩")

st.title("🥩 识肉君 (MeatMaster)")
st.caption("由 Google Gemini 驱动 - 永久在线版")

# --- 智能 Key 管理逻辑 ---
# 1. 优先尝试从云端后台(Secrets)获取 Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.success("✅ 已连接云端服务器，可直接使用！")
except:
    # 2. 如果后台没配 Key，则在侧边栏让用户输入
    api_key = None
    with st.sidebar:
        st.header("🔑 验证")
        api_key = st.text_input("请输入 Google API Key", type="password")
        st.markdown("[👉 点击免费申请 Key](https://aistudio.google.com/app/apikey)")
        st.info("提示：如果你是开发者，请在 Streamlit Secrets 中配置 GOOGLE_API_KEY 以隐藏此输入框。")

# --- 核心分析函数 ---
def analyze_meat(image_file, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt_text = """
    你是一位经验丰富的老屠夫和米其林大厨。请分析这张肉类图片：
    1. **识别**：这是什么动物的哪个具体部位？(例如：猪梅花肉、牛上脑)
    2. **特征**：分析它的肥瘦比、筋膜情况。
    3. **烹饪建议**：适合什么做法？(煎、炒、炖、煮？)
    4. **推荐菜谱**：推荐 3 道最适合这个部位的经典菜。
       - 对于每道菜，请生成一个 Bilibili 和 YouTube 的搜索链接 Markdown 格式，格式如下：
       - [菜名] - [B站视频](https://search.bilibili.com/all?keyword=菜名+教程) / [YouTube](https://www.youtube.com/results?search_query=菜名+recipe)
    
    请用 Markdown 格式输出，多用 Emoji。
    """
    
    try:
        img = Image.open(image_file)
        response = model.generate_content([prompt_text, img])
        return response.text
    except Exception as e:
        return f"❌ 错误: {str(e)}"

# --- 用户交互区 ---
tab1, tab2 = st.tabs(["🖼️ 上传图片", "📷 实时拍照"])
img_file = None

with tab1:
    uploaded_file = st.file_uploader("选择一张肉类图片", type=["jpg", "png", "jpeg", "webp"])
    if uploaded_file: img_file = uploaded_file

with tab2:
    camera_file = st.camera_input("点击拍照")
    if camera_file: img_file = camera_file

# --- 执行逻辑 ---
if img_file:
    st.image(img_file, caption="待识别的肉肉", use_container_width=True)
    
    if st.button("🚀 开始识别", type="primary"):
        if not api_key:
            st.warning("⚠️ 请先在侧边栏输入 API Key！")
        else:
            with st.spinner("正在连接云端大脑分析中..."):
                result = analyze_meat(img_file, api_key)
                st.markdown("### 🧠 分析报告")
                st.markdown(result)
                if "❌" not in result:
                    st.balloons()