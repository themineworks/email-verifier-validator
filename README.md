# Email Verifier & Validator: Bulk MX + SMTP Check

Verify any list of email addresses in bulk with no API key required. Checks syntax, DNS MX records, SMTP mailbox acceptance, disposable domain detection, role-based address tagging, and catch-all heuristics. Returns a clear valid / invalid / risky / unknown verdict per address. Use it as an MCP server in Claude, ChatGPT and any AI agent.

**Run it on Apify:** [apify.com/themineworks/email-verifier-validator](https://apify.com/themineworks/email-verifier-validator)
**Docs, FAQ and pricing:** [themineworks.com/actors/email-verifier-validator](https://themineworks.com/actors/email-verifier-validator/)

**Price:** $2.50 per 1,000 emails on Apify's free plan, down to $1.50 on higher plans. Failed and empty results are never charged.

## What it returns

* DNS MX + SMTP mailbox check
* Disposable domain detection (60+ providers)
* Catch-all heuristic probe
* Role-based address tagging (info@, sales@…)
* Zero charge on syntax failures

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/email-verifier-validator").call(run_input={
    "emails": [
        "test@stripe.com",
        "ceo@notion.so"
    ]
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/email-verifier-validator').call({
    "emails": [
        "test@stripe.com",
        "ceo@notion.so"
    ]
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~email-verifier-validator/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"emails": ["test@stripe.com", "ceo@notion.so"]}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 email_verifier_validator.py --token YOUR_APIFY_TOKEN --emails "test@stripe.com,ceo@notion.so"
node email_verifier_validator.mjs --token YOUR_APIFY_TOKEN --emails "test@stripe.com,ceo@notion.so"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `emails` (required) | array |  | List of email addresses to validate (one per line), for example "jane@acmecorp.com" |
| `checkMx` | boolean | `true` | Resolve the domain's DNS MX records to confirm it can receive mail |
| `checkSmtp` | boolean | `true` | Open a connection to the domain's mail server and run a HELO / MAIL FROM / RCPT TO handshake to test whether… |
| `detectDisposable` | boolean | `true` | Flag addresses on known throwaway / temporary-mailbox domains (mailinator.com, 10minutemail.com… |
| `detectRoleBased` | boolean | `true` | Flag generic role mailboxes (info@, sales@, admin@, support@, etc.) that are not tied to a single person |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `email` | string | The email address that was checked (lowercased, trimmed) |
| `isValidSyntax` | boolean | Whether the address passes RFC-style syntax validation |
| `mxFound` | boolean | Whether the domain has at least one DNS MX record |
| `smtpAccepts` | boolean | Whether the mail server accepted RCPT TO for this mailbox |
| `isDisposable` | boolean | Whether the domain is a known disposable / throwaway mailbox provider |
| `isRoleBased` | boolean | Whether the local-part is a generic role mailbox (info, sales, admin, support, etc.) |
| `isCatchAll` | boolean | Heuristic: the server appears to accept all addresses on the domain, so an accepted RCPT does not prove the… |
| `status` | string | Overall verdict: valid, invalid, risky, or unknown |
| `reason` | string | Short human-readable explanation of the status |
| `domain` | string | The domain portion of the email |
| `checkedAt` | string | ISO timestamp when this address was checked |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/email-verifier-validator
```

## FAQ

### How does the email verification work?

For each address the actor runs four checks in sequence: syntax validation, DNS MX lookup to confirm the domain accepts mail, an optional SMTP RCPT handshake to test the specific mailbox, and a catch-all probe to check whether the server accepts any address regardless of mailbox existence. The verdict combines all four signals.

### Will SMTP verification always work?

No. Port 25 is often firewalled by cloud providers including Apify. When SMTP is blocked or times out the actor returns status "unknown" rather than "valid". It never upgrades an unconfirmed address to valid. You still get the MX result and disposable/role flags.

### What is a catch-all domain?

A catch-all mail server accepts RCPT TO for any address, real or invented, at that domain. When the actor detects this it downgrades the verdict to "risky" because a positive SMTP response no longer proves the mailbox exists.

### How am I charged?

Pay-per-result: $0.001 per verified email address. Addresses that fail syntax checking or verification are never charged.

### How much does the Email Verifier & Validator cost?

$2.50 per 1,000 emails on Apify's free plan, down to $1.50 on higher plans. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [B2B Leads Finder](https://themineworks.com/actors/b2b-leads-finder/): Business emails and LinkedIn profiles for target companies
* [LinkedIn Company Scraper](https://themineworks.com/actors/linkedin-company-details/): Company size, industry, website, and followers without login
* [Zillow Rental Listings Scraper](https://themineworks.com/actors/zillow-rental-listings/): Scrape Zillow for-rent listings by city or zip. $1 per 1,000 results

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
