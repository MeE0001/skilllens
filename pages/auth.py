import streamlit as st
from database.supabase_client import sign_in, sign_up, get_profile
from modules.skill_analyzer import get_all_roles

def show_auth():

    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
font-family:'Inter',sans-serif !important;
}

.stApp{
background:#EDEADE !important;
}

.block-container{
padding-top:0 !important;
padding-left:0 !important;
padding-right:0 !important;
max-width:100% !important;
}

.auth-left-panel{
position:fixed;
top:0;
left:0;
width:42%;
height:100vh;
background:#1A3C23;
padding:5rem 4rem;
display:flex;
flex-direction:column;
justify-content:center;
box-sizing:border-box;
}
                

/* ALIGN STREAMLIT FORM WITH WELCOME TEXT */
[data-testid="stHorizontalBlock"]{
margin-left:11rem;
}

</style>

<div>

<div class="auth-left-panel">

<div style="font-family:'Fraunces',serif;font-style:italic;font-size:1.2rem;
font-weight:400;color:rgba(237,234,222,0.5);margin-bottom:5rem;">
SkillLens
</div>

<div style="font-family:'Fraunces',serif;font-size:3.6rem;font-weight:300;
color:#EDEADE;line-height:1.05;margin-bottom:2rem;">
Your career<br>
clarity<br>
<em style="font-weight:600;">starts here.</em>
</div>

<div style="width:40px;height:1px;background:rgba(237,234,222,0.25);margin-bottom:2rem;"></div>

<div style="font-size:0.88rem;color:rgba(237,234,222,0.45);line-height:1.8;max-width:320px;">
Understand exactly where you stand against any tech role — and get a clear path forward.
</div>

</div>

</div>
""", unsafe_allow_html=True)


    st.markdown("""
<div style="margin-left:45%; padding-top:5rem;">

<h2 style="font-family:Fraunces,serif;color:#1A3C23;">Welcome</h2>

<p style="font-size:0.82rem;color:rgba(26,60,35,0.4);margin-bottom:2rem;">
Sign in or create your free account
</p>

</div>
""", unsafe_allow_html=True)


    left_space, form_col, right_space = st.columns([1.5,2,1])

    with form_col:

        st.markdown("""
        <div style="max-width:420px;margin:auto;">
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign In","Create Account"])

        with tab1:

            email = st.text_input("Email",placeholder="you@example.com",key="si_email")
            password = st.text_input("Password",type="password",placeholder="••••••••",key="si_pass")

            if st.button("Sign In →",type="primary",use_container_width=True):

                if not email or not password:
                    st.error("Please fill in all fields.")

                else:

                    res, err = sign_in(email,password)

                    if err or not res or not res.user:
                        st.error("Invalid email or password.")

                    else:

                        profile = get_profile(res.user.id)

                        st.session_state.user = res.user
                        st.session_state.user_id = res.user.id
                        st.session_state.user_name = profile["name"] if profile else email
                        st.session_state.user_email = email
                        st.session_state.logged_in = True
                        st.session_state.current_page = "Home"
                        st.session_state.access_token = res.session.access_token
                        st.session_state.refresh_token = res.session.refresh_token

                        st.rerun()


        with tab2:

            roles = get_all_roles()

            name = st.text_input("Full Name",placeholder="Your name",key="su_name")
            email_su = st.text_input("Email",placeholder="you@example.com",key="su_email")
            password_su = st.text_input("Password",type="password",placeholder="Min 6 characters",key="su_pass")

            col1, col2 = st.columns([1,1], gap="small")

            with col1:
                exp = st.selectbox(
                    "Experience",
                    ["Student","Fresher","1-2 yrs","3-5 yrs","5+ yrs"],
                    key="su_exp"
                )

            with col2:
                target = st.selectbox(
                    "Target Role",
                    roles,
                    key="su_role"
                )
            if st.button("Create Account →",type="primary",use_container_width=True,key="su_btn"):

                if not all([name,email_su,password_su]):
                    st.error("Please fill in all fields.")

                elif len(password_su) < 6:
                    st.error("Password must be at least 6 characters.")

                else:

                    res, err = sign_up(email_su,password_su,name,exp,target)

                    if err:
                        st.error(f"Error: {err}")

                    elif res and res.user:
                        st.success("Account created! Sign in to continue.")

                    else:
                        st.error("Something went wrong.")

        st.markdown("</div>", unsafe_allow_html=True)