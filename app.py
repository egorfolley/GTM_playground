import streamlit as st
import anthropic
import os
import re
import json
import time
from dotenv import load_dotenv
from agents import scraper, signals, benchmarking, icp, positioning, distribution, actions

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def main():
    pass

if __name__ == "__main__":
    main()
