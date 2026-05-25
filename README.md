# LangChain Agent

A compact, source-aware question-answering Agent built for local development and prompt tuning. It accepts user queries, gathers candidate sources, and returns concise answers with cited references 

## Getting Started / Installation

Follow these steps to run the project locally on Windows.

1. Clone the repository

    ```bash
    git clone https://github.com/yourusername/LangChain_project.git
    cd LangChain_project
    ```

2. Create and activate a virtual environment

    PowerShell:

    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

    CMD:

    ```cmd
    python -m venv .venv
    .\.venv\Scripts\activate.bat
    ```

3. Install dependencies

    ```bash
    uv sync
    ```

4. Configure environment variables

    Copy the example environment file and populate it with your credentials:

    ```bash
    cp .env.example .env
    # then edit .env and add your API keys (OPENAI_API_KEY etc.)
    ```

    If you're on Windows and don't have `cp`, you can copy the file in Explorer or use PowerShell:

    ```powershell
    Copy-Item .env.example .env
    # then open .env in an editor and add your keys
    ```

5. Run the agent

    Start the project using `uv` (recommended) which will use the project's run scripts:

    ```bash
    uv run
    # fallback (if you prefer):
    python main.py
    # or
    python agent.py
    ```

## Tech Stack

- **Language**: Python 3.10+
- **LLM Provider**: Gemini-compatible APIs (set via `GEMINI_API_KEY`) — easily swappable with other providers
- **Framework**: LangChain
- **Entry points**: `main.py`, `agent.py`, prompt templates in `prompts.py`

## Project Layout / Where to Look

- `main.py` — local runner / CLI entrypoint
- `agent.py` — agent orchestration logic
- `prompts.py` — prompt templates and instructions
- `pyproject.toml` — package metadata and dependency spec

---

## Prompt Examples

<details>
<summary><b>Query: What does the acronym "URL" stand for in web addresses?</b></summary>

**Response**: Here are the sources I found. Which ones should I include in the summary?
  1. What does the acronym "URL" stand for in the context of the internet? — https://testbook.com/question-answer/what-does-the-acronym-url-stand-for-in--69709a7c535cd0f2e9ca3145
  2. What does 'URL' stand for? - Uniform Resource Locator - Quora — https://www.quora.com/What-does-URL-stand-for-12
  3. What is the full form of URL? - Facebook — https://www.facebook.com/ImproveEnglishSkills121/posts/what-is-the-full-form-of-url/1172811844849512
  4. URL - Wikipedia — https://en.wikipedia.org/wiki/URL
  5. Tech Tips: What is a URL? - Oak Park Public Library — https://www.oppl.org/news-events/digital-learning/tech-tips-what-is-a-url

**Your selection**: 1, 4

The acronym "URL" stands for Uniform Resource Locator. This is a reference or address used to access a resource on the World Wide Web, essentially acting as a web address.

Sources:
- https://testbook.com/question-answer/what-does-the-acronym-url-stand-for-in--69709a7c535cd0f2e9ca3145
- https://en.wikipedia.org/wiki/URL
</details>

<details>
<summary><b>Query: Which ocean is the largest and deepest on Earth?</b></summary>

**Response**: Here are the sources I found. Which ones should I include in the summary?
  1. Top 10 Deepest Oceans and Seas in the World — https://www.infoplease.com/top-10s/top-10-deepest-oceans-and-seas
  2. How big is the Pacific Ocean? - NOAA Ocean Exploration — https://oceanexplorer.noaa.gov/ocean-fact/pacific-size
  3. What is the largest ocean basin on Earth? — https://oceanservice.noaa.gov/facts/biggestocean.html
  4. Answer without Google What is the deepest ocean on Earth?? — https://www.facebook.com/groups/1572893699951268/posts/2109314366309196
  5. Mariana Trench - Wikipedia — https://en.wikipedia.org/wiki/Mariana_Trench

**Your selection**: https://www.infoplease.com/top-10s/top-10-deepest-oceans-and-seas

The Pacific Ocean is the largest and deepest ocean on Earth. It covers more than 155 million square kilometers (60 million square miles) and contains the Mariana Trench, which includes the Challenger Deep, the lowest known point on Earth's seabed at about 36,200 feet (11,034 meters) below sea level.

Sources:
- https://www.infoplease.com/top-10s/top-10-deepest-oceans-and-seas
</details>

<details>
<summary><b>Query: Is water wet?</b></summary>

**Response** Here are the sources I found. Which ones should I include in the summary?
  1. Is Water Wet? | Fluoride Filter Water Bottles & Pitchers to Remove Contaminants – Clearly Filtered — https://clearlyfiltered.com/articles/is-water-wet
  2. Is water considered wet? - Facebook — https://www.facebook.com/groups/44556868120/posts/10162174144023121
  3. Why is water wet? | Notes and Queries | guardian.co.uk — https://www.theguardian.com/notesandqueries/query/0,5753,-1725,00.html
  4. "Is water wet?" ANSWERED - YouTube — https://www.youtube.com/shorts/cs0_0V2LSNQ
  5. Is Water Wet? : r/chemistry - Reddit — https://www.reddit.com/r/chemistry/comments/82c954/is_water_wet
</details>

<details>
<summary><b>Query: What is 2+2?</b></summary>

**Response**:
  1. Basic Arithmetic #BasicArithmetic /2x2 2+2 2+2 - Facebook — https://www.facebook.com/groups/1003467440405674/posts/1957879411631134
  2. What is the meaning of '2+2' from a mathematical point of view? — https://www.quora.com/What-is-the-meaning-of-2-2-from-a-mathematical-point-of-view
  3. 2 + 2 divided 2 =? MANY will get this BASIC Math Problem WRONG! — https://www.youtube.com/watch?v=TulGFOA-Bn8
  4. Basic Math Skills, Grade 2: Evan Moor - Amazon.com — https://www.amazon.com/Basic-Math-Skills-Grade-2/dp/1557998973
  5. Basic Math Review — https://southbend.iu.edu/students/academic-success-programs/academic-centers-for-excellence/docs/Basic%20Math%20Review%20Card.pdf

**Your selection**: All sources

From a mathematical perspective, "2+2" means to add the real number two to itself. Basic arithmetic involves operations such as addition.

Sources:
* https://www.facebook.com/groups/1003467440405674/posts/1957879411631134
* https://www.quora.com/What-is-the-meaning-of-2-2-from-a-mathematical-point-of-view
* https://www.youtube.com/watch?v=TulGFOA-Bn8
* https://www.amazon.com/Basic-Math-Skills-Grade-2/dp/1557998973
* https://southbend.iu.edu/students/academic-success-programs/academic-centers-for-excellence/docs/Basic%20Math%20Review%20Card.pdf
</details>