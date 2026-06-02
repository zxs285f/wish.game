import streamlit as st
import requests
import time
import random
from io import BytesIO
from PIL import Image
import dashscope
from dashscope import ImageSynthesis

# =====================填入你的通义万相API密钥=====================
import os
DASHSCOPE_KEY = os.environ["DASHSCOPE_KEY"]
dashscope.api_key = DASHSCOPE_KEY

# 页面配置
st.set_page_config(
    page_title="星途旅人",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
header {visibility: hidden;}
/* 星空动态背景 */
.stApp {
background:#050121;
background-image:
radial-gradient(2px 2px at 20px 30px,#ffffff,rgba(0,0,0,0)),
radial-gradient(2px 2px at 40px 70px,#fff,rgba(0,0,0,0)),
radial-gradient(1px 1px at 90px 40px,#fff,rgba(0,0,0,0));
background-repeat:repeat;
background-size:200px 200px;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
    40% {transform: translateY(-10px);}
    60% {transform: translateY(-5px);}
}
.fade-in {animation: fadeIn 0.5s ease-in-out;}
.bounce {animation: bounce 1s;}
/* 按钮浅色适配深色星空 */
.stButton>button {
    border-radius: 12px;
    transition: all 0.3s ease;
    font-size: 16px;
    padding: 12px 20px;
    background:#222752;
    color:#fff;
    border:1px solid #7986ff;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px #8996ff70;
}
.stButton>button:active {
    transform: scale(0.95);
}
/* 正文文字白色适配星空 */
.stMarkdown, .stText, .stCaption, label {
color:#ffffff;
}
@media (max-width: 768px) {
    .stButton>button {
        width: 100%;
        height: 55px;
        font-size: 18px;
        margin: 10px 0;
    }
    .stMarkdown {
        font-size: 17px;
        line-height: 1.6;
    }
    h1, h2, h3 {text-align: center; color:#fff;}
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 优化：移除所有惊喜、礼物相关文案
loading_slogans = [
    "正在整合你的各项选择信息...",
    "正在汇总旅途收集的全部偏好...",
    "系统正在整理本次星际旅程数据...",
    "正在归档你的旅途记录...",
    "数据整理中，请稍作等候...",
    "正在梳理你挑选的全部元素...",
    "整合配色、喜好与场景信息...",
    "马上完成内容汇总...",
    "旅途信息正在最后排版...",
    "各项数据即将整理完毕"
]

game_levels = [
    {
        "level": 1,
        "title": "第一章：飞船启航",
        "story": "欢迎登上星际旅人号！请选择你的飞船涂装和吉祥物，它们将陪你完成这次奇妙的宇宙旅行。",
        "sections": [
            {
                "name": "飞船涂装",
                "options": [
                    {"text": "🌅 暖橙色日落", "tags": ["暖橙色", "温暖", "活力", "日落"]},
                    {"text": "🌊 冰蓝色海洋", "tags": ["冰蓝色", "清新", "宁静", "海洋"]},
                    {"text": "🌿 薄荷绿森林", "tags": ["薄荷绿", "治愈", "自然", "森林"]},
                    {"text": "🎨 都不戳我？那笔给你自己画_", "custom": True, "topic": "颜色", "prompt": "快写下你最爱的颜色吧～"}
                ],
                "success_msg": "🎨 收到！这就给你的飞船喷上这个颜色～"
            },
            {
                "name": "飞船吉祥物",
                "options": [
                    {"text": "🐱 软萌猫咪", "tags": ["猫咪", "可爱", "软萌", "治愈"]},
                    {"text": "🐶 活泼小狗", "tags": ["小狗", "活泼", "忠诚", "阳光"]},
                    {"text": "🐰 可爱兔子", "tags": ["兔子", "温柔", "可爱", "纯洁"]},
                    {"text": "🐾 没有我的本命？那你写一个_", "custom": True, "topic": "动物", "prompt": "快写下你最爱的小动物吧～"}
                ],
                "success_msg": "🐾 好嘞！这个小可爱现在是你的专属船员啦～"
            }
        ]
    },
    {
        "level": 2,
        "title": "第二章：星际补给站",
        "story": "飞船需要补充能量啦！宇宙小卖部什么都有，请选择你喜欢的饮品和零食，我们马上为你准备好。",
        "sections": [
            {
                "name": "能量饮品",
                "options": [
                    {"text": "☕ 热拿铁", "tags": ["拿铁", "咖啡", "温暖", "醇香"]},
                    {"text": "🍵 冰绿茶", "tags": ["绿茶", "清爽", "健康", "淡雅"]},
                    {"text": "🥤 鲜榨果汁", "tags": ["果汁", "酸甜", "新鲜", "水果"]},
                    {"text": "☕ 这些都一般？那你点单_", "custom": True, "topic": "饮品", "prompt": "宇宙小卖部什么都有哦～"}
                ],
                "success_msg": "☕ 马上安排！宇宙最快外卖送达～"
            },
            {
                "name": "星际零食",
                "options": [
                    {"text": "🍫 巧克力坚果", "tags": ["巧克力", "坚果", "浓郁", "香甜"]},
                    {"text": "🍓 草莓软糖", "tags": ["草莓", "软糖", "酸甜", "可爱"]},
                    {"text": "🍵 抹茶饼干", "tags": ["抹茶", "饼干", "清香", "酥脆"]},
                    {"text": "🍬 没有想吃的？那你报菜名_", "custom": True, "topic": "零食/口味", "prompt": "想吃什么尽管说～"}
                ],
                "success_msg": "🍬 收到！已经装进你的零食背包啦～"
            }
        ]
    },
    {
        "level": 3,
        "title": "第三章：目的地选择",
        "story": "前方探测到四颗美丽的星球，每一颗都有独特的风景。你想先去哪里探索呢？",
        "sections": [
            {
                "name": "目的地星球",
                "options": [
                    {"text": "🌸 春日花星球（微风，赏花野餐）", "tags": ["春天", "花朵", "浪漫", "野餐"]},
                    {"text": "🏖️ 夏日海星球（阳光，沙滩游泳）", "tags": ["夏天", "大海", "阳光", "沙滩"]},
                    {"text": "🍁 秋日枫星球（落叶，散步拍照）", "tags": ["秋天", "枫叶", "文艺", "散步"]},
                    {"text": "❄️ 冬日雪星球（飘雪，堆雪人）", "tags": ["冬天", "雪花", "纯洁", "玩雪"]},
                    {"text": "🌍 这些星球都去过？那你说去哪_", "custom": True, "topic": "季节/地点", "prompt": "想去哪里宇宙都带你去～"}
                ],
                "success_msg": "🌍 航线已设定！我们这就出发～"
            }
        ]
    },
    {
        "level": 4,
        "title": "第四章：心愿星球",
        "story": "最后一站我们来到了传说中能实现愿望的心愿星球。每个星际旅人都可以在这里许一个愿望，它会被宇宙永远记录下来。",
        "sections": [
            {
                "name": "你的愿望",
                "options": [
                    {"text": "😊 希望每天都开心快乐", "tags": ["开心", "快乐", "乐观", "简单"]},
                    {"text": "✈️ 希望能去更多地方旅行", "tags": ["旅行", "自由", "探索", "冒险"]},
                    {"text": "💖 希望身边的人都幸福", "tags": ["幸福", "家人", "朋友", "温暖"]},
                    {"text": "✨ 这些愿望太小？那你许个大的_", "custom": True, "topic": "愿望", "prompt": "你的愿望宇宙一定会听到的～"}
                ],
                "success_msg": "✨ 愿望已签收！宇宙正在加急处理中～"
            }
        ]
    }
]

# 文本生成祝福语
def call_llm_api(prompt, temperature=0.7, max_tokens=500):
    return None

def ai_check_content(user_input, topic):
    return True, "默认通过"

def ai_extract_tags(user_input, topic):
    return [user_input]

def generate_birthday_content(all_tags):
    return """🎂 你的专属生日蛋糕：
根据你的喜好定制配色、水果与装饰，造型精致用料新鲜。
💌 生日祝福：
🎉 生日快乐！我最亲爱的朋友！愿岁岁平安，日日欢喜，万事顺遂。"""

# 通义万相生成蛋糕图片
def generate_cake_img(all_tags):
    base = "写实生日蛋糕，柔和马卡龙配色，暖光氛围感，高清4K，无多余文字，精致奶油裱花"
    p_list = [base]
    for t in all_tags:
        if any(x in t for x in ["色","橙","蓝","绿","粉","紫","白"]):
            p_list.append(f"主体色调{t}")
        if any(x in t for x in ["草莓","芒果","蓝莓","水蜜桃","樱桃"]):
            p_list.append(f"点缀新鲜{t}果肉")
        if any(x in t for x in ["巧克力","抹茶","芋泥"]):
            p_list.append(f"{t}奶油内馅")
        if any(x in t for x in ["春天","夏日","秋天","冬日"]):
            p_list.append(f"画面融入{t}氛围")
    prompt = "，".join(p_list)
    try:
        rsp = ImageSynthesis.call(model="wanx-v1", prompt=prompt, size="1024*1024")
        img_url = rsp.output.results[0].url
        img_bin = requests.get(img_url,timeout=20).content
        return Image.open(BytesIO(img_bin))
    except Exception:
        return None

# 状态初始化
if 'current_level' not in st.session_state:
    st.session_state.current_level = 0
if 'current_section' not in st.session_state:
    st.session_state.current_section = 0
if 'collected_tags' not in st.session_state:
    st.session_state.collected_tags = []
if 'game_complete' not in st.session_state:
    st.session_state.game_complete = False
if 'show_custom_input' not in st.session_state:
    st.session_state.show_custom_input = False
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

# 侧边实时选择反馈
with st.sidebar:
    st.subheader("📋 你的已选偏好清单")
    if st.session_state.collected_tags:
        for item in list(set(st.session_state.collected_tags)):
            st.markdown(f"- {item}")
    else:
        st.info("尚未选择任何内容，快去挑选吧！")

# 主逻辑
if not st.session_state.game_complete:
    # 侧边栏实时展示已选内容【选择即时反馈】
    with st.sidebar:
        st.subheader("📋 你的已选偏好清单")
        if st.session_state.collected_tags:
            for item in list(set(st.session_state.collected_tags)):
                st.markdown(f"- {item}")
        else:
            st.info("尚未选择任何内容，快去挑选吧！")

    total_sec = sum(len(i["sections"]) for i in game_levels)
    now_proc = (st.session_state.current_level*2 + st.session_state.current_section)/total_sec
    st.progress(now_proc)
    st.caption(f"进度：{int(now_proc*100)}%")

    st.title("🚀 星途旅人")
    st.divider()
    lv = game_levels[st.session_state.current_level]
    sec = lv["sections"][st.session_state.current_section]
    st.subheader(lv["title"])
    st.write(lv["story"])
    st.subheader(f"选择你的{sec['name']}：")

    for idx,opt in enumerate(sec["options"]):
        if st.button(opt["text"],key=f"{st.session_state.current_level}_{st.session_state.current_section}_{idx}"):
            if opt.get("custom"):
                st.session_state.show_custom_input=True
                st.session_state.current_topic=opt["topic"]
                st.session_state.current_prompt=opt["prompt"]
                st.session_state.current_succ=sec["success_msg"]
            else:
                st.session_state.collected_tags.extend(opt["tags"])
                st.session_state.feedback = sec["success_msg"]
                st.session_state.current_section +=1
                if st.session_state.current_section >= len(lv["sections"]):
                    st.session_state.current_section=0
                    st.session_state.current_level +=1
                if st.session_state.current_level >= len(game_levels):
                    st.session_state.game_complete=True
            st.rerun()

    if st.session_state.show_custom_input:
        user_txt = st.text_input(st.session_state.current_prompt,max_chars=30,key="cus_in")
        if user_txt:
            ok,reason = ai_check_content(user_txt,st.session_state.current_topic)
            if ok:
                st.success(st.session_state.current_succ)
                tag_list = ai_extract_tags(user_txt,st.session_state.current_topic)
                st.session_state.collected_tags.extend(tag_list)
                st.session_state.current_section +=1
                if st.session_state.current_section >= len(lv["sections"]):
                    st.session_state.current_section=0
                    st.session_state.current_level +=1
                if st.session_state.current_level >= len(game_levels):
                    st.session_state.game_complete=True
                st.session_state.show_custom_input=False
                time.sleep(1)
                st.rerun()
            else:
                st.error("哎呀，这个好像和我们现在要选的不太一样呢～再想想看？")
    if st.session_state.feedback:
        st.success(st.session_state.feedback)
        st.session_state.feedback=""

else:
    st.title("🎉 恭喜你完成了星际旅行！")
    st.write("基于你的所有选择，我们为你生成了一份专属的星际旅行报告...")
    load_place = st.empty()
    pro_bar = st.progress(0)

    # 进度走完的同时同步生成图片+文案，预加载存变量
    with st.spinner(""):
        cake_img = generate_cake_img(st.session_state.collected_tags)
        text_res = generate_birthday_content(st.session_state.collected_tags)

    # 进度动画照常播放
    for i in range(20):
        load_place.markdown(f"✨ {random.choice(loading_slogans)}")
        pro_bar.progress((i+1)/20)
        time.sleep(0.3)
    load_place.empty()
    pro_bar.empty()

    st.balloons()
    time.sleep(0.5)
    st.snow()
    st.markdown("---")
    st.write("但是...")
    time.sleep(1)
    st.write("这份报告好像有点特别...")
    time.sleep(1)
    st.write("因为它其实是...")
    time.sleep(1.5)
    st.title("🎂 生日快乐！朋友！")
    st.markdown("---")

    # 进度结束，图片+祝福语同时渲染出来
    col1, col2 = st.columns([1,1])
    with col1:
        if cake_img:
            st.image(cake_img, caption="你的专属定制蛋糕", width='stretch')
        else:
            st.image("https://picsum.photos/id/292/800/600", caption="备用蛋糕图", width='stretch')
            st.info("图片生成临时异常，使用备用蛋糕")

    with col2:
        st.subheader("📝 旅途收集全记录")
        tag_set = list(set(st.session_state.collected_tags))
        st.markdown("**你的全部喜好汇总：**")
        st.write("、".join(tag_set))
        st.divider()
        st.subheader("💌 生日寄语")
        st.markdown(text_res)

    st.markdown("### ✨ 星际旅途收尾寄语")
    st.write("希望未来每一时光都恰如此刻喜悦")
    st.markdown("---")
    st.success("希望你喜欢这份独一无二的旅途总结！❤️")

    if st.button("🔄 再玩一次"):
        st.session_state.clear()
        st.rerun()
