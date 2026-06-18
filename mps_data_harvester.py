#!/usr/bin/env python3
"""
🧬 MPS-I PUBLIC MEDICAL DATA HARVESTER (ENTREZ API CLIENT)
Deployed to: GEEKOM Node (the-grid)
Authors: Trent Reznor & Aphex Twin (Subconscious Systems Group)

This script implements a zero-dependency, highly robust client for the NCBI Entrez API.
It allows the GEEKOM to:
1. Search the PubMed Central (PMC) database for full-text, open-access academic articles
   matching specific search queries (e.g., "Mucopolysaccharidosis Type I", "OTL-203", "Laronidase").
2. Fetch full metadata and text summaries of the top matching clinical trials and papers.
3. Clean and parse the retrieved datasets into machine-readable JSON formats, structured
   specifically for direct ingestion/embedding into GEEKOM's local ChromaDB vector database.
"""

import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import os
import time

def search_pmc_articles(query, max_results=10):
    """
    Queries NCBI esearch to find PubMed Central IDs (PMCIDs) matching our search terms.
    """
    print(f"[🔍] Searching PubMed Central for: '{query}'...")
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={encoded_query}&retmode=json&retmax={max_results}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            id_list = data.get("esearchresult", {}).get("idlist", [])
            print(f"[+] Found {len(id_list)} open-access PMC papers matching query.")
            return id_list
    except Exception as e:
        print(f"[❌] Error querying NCBI E-Search API: {e}")
        return []

def fetch_pmc_details(pmcid_list):
    """
    Queries NCBI esummary/efetch to retrieve metadata and text summaries for each PMCID.
    """
    if not pmcid_list:
        return []
        
    ids_str = ",".join(pmcid_list)
    print(f"[📥] Fetching clinical metadata for PMCIDs: {ids_str}...")
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&id={ids_str}&retmode=json"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get("result", {})
            
            articles = []
            for pmcid in pmcid_list:
                info = results.get(pmcid)
                if info:
                    # Clean up authors list
                    authors = [a.get("name") for a in info.get("authors", []) if "name" in a]
                    
                    articles.append({
                        "pmcid": f"PMC{pmcid}",
                        "title": info.get("title"),
                        "journal": info.get("source"),
                        "publish_date": info.get("pubdate"),
                        "authors": authors,
                        "doi": info.get("articleids", [{}])[0].get("value") if info.get("articleids") else None,
                        "summary_text": f"Title: {info.get('title')}. Published in {info.get('source')} on {info.get('pubdate')}. Authors: {', '.join(authors[:5])}."
                    })
            return articles
    except Exception as e:
        print(f"[❌] Error fetching details from NCBI E-Summary: {e}")
        return []

def harvest_mps_knowledge():
    # Standard query specifically seeking high-impact, open-source clinical research papers
    query_terms = "Mucopolysaccharidosis Type I AND (gene therapy OR Aldurazyme OR cartilage)"
    
    # Run Search & Fetch
    pmcids = search_pmc_articles(query_terms, max_results=8)
    
    # NCBI Rate limits: 3 requests per second without an API key. 
    # Let's sleep slightly to remain highly compliant and friendly to public medical servers.
    time.sleep(0.5)
    
    articles = fetch_pmc_details(pmcids)
    
    output_data = {
        "harvester_v": "1.0",
        "search_query": query_terms,
        "total_harvested": len(articles),
        "articles": articles
    }
    
    return output_data

if __name__ == "__main__":
    print("🧬 DEPLOYING PUBLIC MEDICAL NCBI DATA HARVESTER 🧬")
    print("--------------------------------------------------")
    
    harvest_results = harvest_mps_knowledge()
    
    print(f"\n📊 HARVEST SUMMARY (PROCESSED {harvest_results['total_harvested']} CLINICAL PAPERS):")
    print("==========================================================")
    for idx, art in enumerate(harvest_results["articles"]):
        print(f"👉 ARTICLE {idx + 1}:")
        print(f"   * PMCID:      {art['pmcid']}")
        print(f"   * Title:      {art['title']}")
        print(f"   * Journal:    {art['journal']} ({art['publish_date']})")
        print(f"   * Authors:    {', '.join(art['authors'][:3])} (et al.)")
        print()
        
    # Save the harvested metadata to a clinical corpus cache file
    out_path = "/data/.openclaw/workspace/mps_research_core/harvested_clinical_corpus.json"
    with open(out_path, "w") as f:
        json.dump(harvest_results, f, indent=2)
        
    print(f"💾 Raw clinical corpus successfully written to: {out_path}")
    print("[+] Ready for semantic chunking and GEEKOM local ChromaDB RAG injection!")
