import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {record} from 'testreel';

const [definition,output]=process.argv.slice(2);
if(!definition || !output) throw Error('Usage: node capture.mjs <definition.json> <new-output-folder>');
try {await fs.access(output);throw Error('Capture output already exists; choose a fresh attempt folder.');}
catch(error) {if(error.code!=='ENOENT')throw error;}
const started=Date.now();
const result=await record(path.resolve(definition),{outputDir:path.resolve(output),keepIntermediates:true});
const video=result.video;
const sourceHash=video?createHash('sha256').update(await fs.readFile(video)).digest('hex'):null;
await fs.writeFile(path.join(output,'capture-receipt.json'),JSON.stringify({elapsed_seconds:(Date.now()-started)/1000,source_sha256:sourceHash,result,visual_review:'pending',note:'An MP4 or returned result does not prove every recorded action succeeded.'},null,2)+'\n');
console.log('Capture returned. Inspect step failures, screenshots and moving footage before accepting. Receipt saved in attempt folder.');
