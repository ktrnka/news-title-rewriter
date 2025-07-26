import os
from pprint import pprint
from openai import OpenAI
from dotenv import load_dotenv


def rewrite_headline(headline: str, snippet: str = "") -> str:
    token = os.environ["GITHUB_TOKEN"]

    print(f"Headline: {headline}")
    print(f"Snippet: {snippet}")

    endpoint = "https://models.github.ai/inference"
    model = "openai/gpt-4.1"
    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You're going to help me rewrite news titles to be more neutral and in plain language, so that I can more easily decide whether I want to read the article. We're attempting to reduce bias and sensationalism in news headlines.

                I'll provide you with a news headline and optional snippet of the article, and you will rewrite the headline to be more neutral and straightforward.
                """,
            },
            {
                "role": "user",
                "content": f"""
                Headline: {headline}
                Snippet: {snippet}""".strip(),
            }
        ],
        temperature=0.3,
        top_p=1.0,
        model=model
    )

    # TODO: Handle type errors (null response, etc.) better
    return response.choices[0].message.content


def main():
    load_dotenv()

    headline = "Is An Elusive Intermediate Mass Black Hole Eating a Star in This Distant Galaxy?"
    snippet = """
Are astronomers on the precipice of discovering the first, elusive, intermediate mass black hole (IMBH)? That's been the case for a while, as different researchers present evidence of them. There's a candidate IMBH in the globular cluster Omega Centauri, and there's evidence that they're near supermassive black holes in galactic centers. Now researchers have found evidence of an IMBH devouring a star.

X-ray emissions are one of the primary ways that astronomers detect black holes. When material from a companion star gets drawn toward a stellar-mass black hole, the material is superheated in an accretion disk and emits x-rays. The same is true for supermassive black holes (SMBH) during tidal disruption events. The same is true for the hypothesized IMBHs and the new candidate.

The Hubble Space Telescope and the Chandra X-ray Observatory worked together to sense bright x-ray emissions from what appears to be an IMBH in a distant elliptical galaxy 450 million light-years away. The discovery is presented in new research titled "Multiwavelength Study of a Hyperluminous X-Ray Source near NGC 6099: A Strong IMBH Candidate," published in The Astrophysical Journal. The lead author is Yi-Chi Chang from the Institute of Astronomy at the National Tsing Hua University in Taiwan.

"We report on the intriguing properties of a variable X-ray source projected at the outskirts of the elliptical galaxy NGC 6099," the authors write. "The optical continuum can be modeled as stellar emission from a compact star cluster or an X-ray-irradiated accretion disk, consistent with the IMBH scenario."

The source is called NGC 6099 HLX-1, and Chandra first detected it in 2009 when it flared brightly in x-rays. Astronomers have been monitoring it with the ESA's XMM-Newton since then and watched as its x-ray emission varied over time. Observations from multiple other telescopes round out the evidence.

Researchers want to find an IMBH because they could be the missing link in the black hole hierarchy.

“X-ray sources with such extreme luminosity are rare outside galaxy nuclei and can serve as a key probe for identifying elusive IMBHs," said lead author Yi-Chi Chang of the National Tsing Hua University, Hsinchu, Taiwan. "They represent a crucial missing link in black hole evolution between stellar mass and supermassive black holes.”
"""

    rewrite = rewrite_headline(headline, snippet)

    print("Rewritten Headline:")
    print(rewrite)

    # TODO
    # 1. Improve the prompt. The results seemed a little worse than what we had in the UI
    # 2. Use Json mode + Pydantic to return a structured response so that we don't have to parse the string, and can easily ignore things like "Neutral, Plain Language Headline:"
    # 3. Take a URL as input and scrape the headline and snippet from the page
    # 4. Add a CLI interface to take input from the command line


if __name__ == "__main__":
    main()
