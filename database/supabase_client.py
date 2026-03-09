import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def _get_authed_client():
    """Return client with current session set, so RLS works."""
    import streamlit as st
    access_token  = st.session_state.get("access_token")
    refresh_token = st.session_state.get("refresh_token", "")
    if access_token:
        try:
            supabase.auth.set_session(access_token, refresh_token)
        except Exception:
            pass
    return supabase


# ── AUTH ──────────────────────────────────────────────

def sign_up(email, password, name, experience_level, target_role):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            supabase.table("profiles").insert({
                "id":               res.user.id,
                "name":             name,
                "email":            email,
                "experience_level": experience_level,
                "target_role":      target_role,
            }).execute()
        return res, None
    except Exception as e:
        return None, str(e)


def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return res, None
    except Exception as e:
        return None, str(e)


def sign_out():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass


def get_current_user():
    try:
        return supabase.auth.get_user()
    except Exception:
        return None


# ── PROFILE ───────────────────────────────────────────

def get_profile(user_id):
    try:
        client = _get_authed_client()
        res = client.table("profiles").select("*").eq("id", user_id).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None


def update_profile(user_id, updates):
    try:
        client = _get_authed_client()
        client.table("profiles").update(updates).eq("id", user_id).execute()
        return True
    except Exception:
        return False


# ── REPORTS ───────────────────────────────────────────

def save_report(user_id, report):
    try:
        client = _get_authed_client()
        client.table("skill_reports").insert({
            "user_id":        user_id,
            "report_name":    report["name"],
            "role":           report["role"],
            "score":          report["score"],
            "matched_skills": report["matched"],
            "missing_skills": report["missing"],
            "readiness":      report["readiness"],
            "salary":         report["salary"],
            "difficulty":     report["difficulty"],
        }).execute()
        return True, None
    except Exception as e:
        return False, str(e)


def get_reports(user_id):
    try:
        client = _get_authed_client()
        res = client.table("skill_reports") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .execute()
        return res.data or []
    except Exception:
        return []


def delete_report(report_id):
    try:
        client = _get_authed_client()
        client.table("skill_reports").delete().eq("id", report_id).execute()
        return True
    except Exception:
        return False