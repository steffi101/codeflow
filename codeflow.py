import streamlit as st

def detect_language(code_text):
    if not code_text.strip():
        return "No code yet"
    
    if 'print(' in code_text or 'def ' in code_text:
        return "🐍 Python"
    elif 'console.log' in code_text or 'function ' in code_text:
        return "🟨 JavaScript"
    else:
        return "❓ Unknown"

def analyze_code(code_text):
    suggestions = []
    
    if not code_text.strip():
        return suggestions
    
    if 'var ' in code_text:
        suggestions.append("⚠️ Use 'let' or 'const' instead of 'var'")
    
    if 'console.log' in code_text:
        suggestions.append("💡 Remove console.log statements before production")
    
    if '==' in code_text and '===' not in code_text:
        suggestions.append("🚨 Use '===' instead of '==' for strict equality")
    
    if 'import *' in code_text:
        suggestions.append("⚠️ Avoid 'import *' - import specific functions")
    
    return suggestions

def calculate_score(code_text, suggestions):
    if not code_text.strip():
        return 0
    score = 100 - (len(suggestions) * 15)
    return max(0, score)

st.title("🔍 CodeFlow")
st.subheader("AI-Powered Code Review Assistant")

# Sample code buttons
st.write("**Try these examples:**")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 Good JavaScript"):
        st.session_state.sample_code = '''const userName = "Alice";
const greeting = `Hello, ${userName}!`;
if (userName === "Alice") {
    // Welcome message
    alert(greeting);
}'''

with col2:
    if st.button("⚠️ Bad JavaScript"):
        st.session_state.sample_code = '''var name = "John";
console.log("Starting app");
console.log(name);
if (name == "John") {
    console.log("Welcome!");
}'''

with col3:
    if st.button("🐍 Python Example"):
        st.session_state.sample_code = '''def calculate_total(items):
    total = 0
    for item in items:
        total += item["price"]
    return total

prices = [{"price": 10}, {"price": 20}]
print(calculate_total(prices))'''

# Get code from text area or sample
code = st.text_area(
    "Paste your code here:", 
    value=st.session_state.get('sample_code', ''),
    height=250
)

if code:
    language = detect_language(code)
    lines = len(code.split('\n'))
    suggestions = analyze_code(code)
    score = calculate_score(code, suggestions)
    
    # Show score prominently
    if score >= 80:
        st.success(f"🎯 Quality Score: {score}/100 - Excellent!")
    elif score >= 60:
        st.warning(f"⚠️ Quality Score: {score}/100 - Good, needs minor fixes")
    else:
        st.error(f"🚨 Quality Score: {score}/100 - Needs improvement")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Language", language)
    with col2:
        st.metric("Characters", len(code))
    with col3:
        st.metric("Lines", lines)
    
    st.write("---")
    st.write("### 🔍 Analysis Results")
    
    if suggestions:
        st.write(f"**Found {len(suggestions)} issues:**")
        for i, suggestion in enumerate(suggestions, 1):
            st.write(f"{i}. {suggestion}")
    else:
        st.success("✅ No issues found! Your code looks clean and follows best practices.")
        
else:
    st.info("👆 Paste code above or try the sample buttons to get started!")
