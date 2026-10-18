import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {normalizeMedia} from './normalize.mjs';

const root=path.dirname(fileURLToPath(import.meta.url));
process.chdir(root);
const python=process.env.DEMO_PYTHON || 'python3';
execFileSync(python,['support/check_project.py',root],{stdio:'inherit'});
const project=JSON.parse(await fs.readFile('project.json','utf8'));
if(project.variants.length!==1 || project.variants[0].id!=='C03' || project.variants[0].engine!=='remotion') throw Error('This starter implements C03 only. Use actual upstream pipelines for other workflow IDs.');
const bin=path.resolve('node_modules/.bin/remotion');
const extra=process.argv.slice(2);
if(extra.length && !(extra.length===2 && extra[0]==='--browser-executable')) throw Error('Supported option: --browser-executable <path>');
await fs.mkdir('outputs',{recursive:true});
await fs.mkdir('receipts',{recursive:true});
const delivery={product:project.product.name,locales:project.locales,formats:project.formats,rows:[]};
await fs.writeFile('delivery.json',JSON.stringify(delivery,null,2)+'\n');
const times=(scene,format)=>format.timing?.[scene.id]??[scene.start,scene.end];
for(const locale of project.locales) {
  const recording=project.recordings[locale.id];
  const source=path.join('public',recording.src);
  const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_format','-of','json',source],{encoding:'utf8'}));
  const sourceHash=createHash('sha256').update(await fs.readFile(source)).digest('hex');
  for(const format of project.formats) {
    for(const scene of project.scenes.filter(s=>s.kind==='product')) {
      const [start,end]=times(scene,format);
      const required=(recording.offset_seconds??0)+(scene.source_start_seconds?.[locale.id]??0)+(end-start);
      if(required>Number(probe.format.duration)+1/format.fps) throw Error('Not enough continuous source footage for '+locale.id+'/'+format.id);
    }
    const key='C03-'+locale.id+'-'+format.id;
    const propsFile='receipts/'+key+'-props.json';
    const src='outputs/'+key+'.mp4';
    const poster='outputs/'+key+'.jpg';
    await fs.writeFile(propsFile,JSON.stringify({project,locale:locale.id,format}));
    const begin=Date.now();
    const args=['render','src/index.ts','ProductDemo',src,'--props='+path.resolve(propsFile),'--codec=h264','--pixel-format=yuv420p','--concurrency=2',...extra];
    execFileSync(bin,args,{stdio:'inherit'});
    const normalization=await normalizeMedia(src);
    execFileSync(bin,['still','src/index.ts','ProductDemo',poster,'--props='+path.resolve(propsFile),'--frame='+Math.min(Math.round(format.fps*.4),Math.round(format.fps*format.duration_seconds)-1),...extra],{stdio:'inherit'});
    const sha256=createHash('sha256').update(await fs.readFile(src)).digest('hex');
    const receipt={key,engine:'remotion',capture_source:recording.source_kind,source_sha256:sourceHash,output_sha256:sha256,elapsed_seconds:(Date.now()-begin)/1000,invocation:['remotion',...args],normalization,shared_edit:false};
    await fs.writeFile('receipts/'+key+'.json',JSON.stringify(receipt,null,2)+'\n');
    delivery.rows.push({id:'C03',name:project.variants[0].name,locale:locale.id,format:format.id,engine:'remotion',src,poster,sha256,source_sha256:sourceHash,receipt:'receipts/'+key+'.json'});
    await fs.writeFile('delivery.json',JSON.stringify(delivery,null,2)+'\n');
  }
}
console.log('Rendered '+delivery.rows.length+' real-source C03 cuts. Run full media and visual verification.');
