#!/usr/bin/env python3
"""Bulk email validation: MX, SMTP, disposable, catch-all detection. Python, Node.js and cURL clients for the Email Verifier & Validator on Apify, pay per result.

Command-line client for the themineworks/email-verifier-validator actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/email-verifier-validator/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/email-verifier-validator"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--emails", help="Comma-separated. List of email addresses to validate (one per line), for example 'jane@acmecorp.com'")
    ap.add_argument("--check-mx", action=argparse.BooleanOptionalAction, help="Resolve the domain's DNS MX records to confirm it can receive mail")
    ap.add_argument("--check-smtp", action=argparse.BooleanOptionalAction, help="Open a connection to the domain's mail server and run a HELO / MAIL FROM / RCPT TO…")
    ap.add_argument("--detect-disposable", action=argparse.BooleanOptionalAction, help="Flag addresses on known throwaway / temporary-mailbox domains (mailinator.com…")
    ap.add_argument("--detect-role-based", action=argparse.BooleanOptionalAction, help="Flag generic role mailboxes (info@, sales@, admin@, support@, etc.) that are not tied to…")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.emails: run_input["emails"] = [s.strip() for s in a.emails.split(",") if s.strip()]
    if a.check_mx is not None: run_input["checkMx"] = a.check_mx
    if a.check_smtp is not None: run_input["checkSmtp"] = a.check_smtp
    if a.detect_disposable is not None: run_input["detectDisposable"] = a.detect_disposable
    if a.detect_role_based is not None: run_input["detectRoleBased"] = a.detect_role_based

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
