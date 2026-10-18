import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';

const stream=file=>JSON.parse(execFileSync('ffprobe',['-v','error','-select_streams','v:0','-show_streams','-of','json',file],{encoding:'utf8'})).streams[0];

export async function normalizeMedia(file) {
  const before=stream(file);
  if(before.pix_fmt==='yuv420p'&&before.color_range!=='pc')return {applied:false,pixel_format:before.pix_fmt,color_range:before.color_range??'unspecified'};
  const temporary=file.replace(/\.mp4$/,'.normalized.mp4');
  if(temporary===file)throw Error('Expected MP4 normalization target');
  const inputRange=before.pix_fmt==='yuvj420p'||before.color_range==='pc'?'pc':'auto';
  const args=['-v','error','-y','-i',file,'-map','0:v:0','-map','0:a?','-vf','scale=in_range='+inputRange+':out_range=tv,format=yuv420p','-c:v','libx264','-crf','18','-preset','fast','-threads','2','-c:a','copy','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',temporary];
  execFileSync('ffmpeg',args,{stdio:'inherit'});
  const after=stream(temporary);
  if(after.pix_fmt!=='yuv420p'||after.color_range!=='tv')throw Error('Normalization output failed pixel-format/range checks');
  await fs.rename(temporary,file);
  return {applied:true,source_pixel_format:before.pix_fmt,source_color_range:before.color_range,pixel_format:after.pix_fmt,color_range:after.color_range,invocation:['ffmpeg',...args]};
}
