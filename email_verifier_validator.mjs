#!/usr/bin/env node
// Node.js client for the themineworks/email-verifier-validator actor on Apify: runs it and saves results.json.
// Flags map 1:1 to the actor's input. Free API token: https://console.apify.com/sign-up
// Docs and pricing: https://themineworks.com/actors/email-verifier-validator/
import { ApifyClient } from 'apify-client';
import { writeFileSync } from 'node:fs';

const ACTOR = 'themineworks/email-verifier-validator';

function parseArgs(argv) {
    const out = {};
    for (let i = 0; i < argv.length; i++) {
        if (!argv[i].startsWith('--')) continue;
        const key = argv[i].slice(2);
        out[key] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    }
    return out;
}

const args = parseArgs(process.argv.slice(2));
const token = args.token || process.env.APIFY_TOKEN;
if (!token) {
    console.error('Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up');
    process.exit(1);
}

const runInput = {};
if (args['emails'] !== undefined) runInput.emails = String(args['emails']).split(',').map((s) => s.trim());
if (args['check-mx'] !== undefined) runInput.checkMx = args['check-mx'] === true || args['check-mx'] === 'true';
if (args['check-smtp'] !== undefined) runInput.checkSmtp = args['check-smtp'] === true || args['check-smtp'] === 'true';
if (args['detect-disposable'] !== undefined) runInput.detectDisposable = args['detect-disposable'] === true || args['detect-disposable'] === 'true';
if (args['detect-role-based'] !== undefined) runInput.detectRoleBased = args['detect-role-based'] === true || args['detect-role-based'] === 'true';

const client = new ApifyClient({ token });
console.log(`Running ${ACTOR} ...`);
const run = await client.actor(ACTOR).call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
writeFileSync('results.json', JSON.stringify(items, null, 2));
console.log(`Saved ${items.length} results to results.json`);
