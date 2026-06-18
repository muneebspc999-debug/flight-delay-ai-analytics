import streamlit as st
from groq import Groq

FLIGHT_CONTEXT = """
US Flight Data (2024):
- Total Flights: 7.1M
- Delayed Flights: 1.4M
- Cancelled Flights: 96K
- On-Time Performance: 80.2%

Cancellation Reasons:
- Weather: 55.66% (54K)
- Carrier: 32.11% (31K)
- National Air System: 12.23% (12K)
- Security: ~0%

Top delayed airports: DFW, DEN, ATL, ORD, CLT, LAS, MCO, PHX, LAX, SEA

Monthly trend: Delays peak in July-August, lowest in September-November.
"""

st.set_page_config(page_title="Flight Delay Assistant", page_icon="✈️")
st.title("✈️ Flight Delay Assistant")
st.caption("Ask questions about US flight delays and cancellations (2024 data)")

api_key = st.text_input("Enter your Groq API key", type="password")
query = st.text_input("Ask a question", placeholder="If today is stormy, how likely is my flight to get cancelled?")

if st.button("Ask") and api_key and query:
    with st.spinner("Thinking..."):
        try:
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a flight analytics assistant. Use this data as your primary source:\n\n{FLIGHT_CONTEXT}\n\nIf the question goes beyond this data, use your general knowledge about US aviation to help the user."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            )
            st.success(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")