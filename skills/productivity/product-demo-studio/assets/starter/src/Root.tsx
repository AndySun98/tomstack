import React from 'react';
import {AbsoluteFill, Audio, Composition, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import config from '../project.json';

type Props = {project: any; locale: string; format: any};
const times = (scene: any, format: any) => format.timing?.[scene.id] ?? [scene.start,scene.end];

const Scene: React.FC<{scene: any; project: any; locale: string; format: any}> = ({scene,project,locale,format}) => {
  const frame=useCurrentFrame();
  const {fps,width,height}=useVideoConfig();
  const copy=scene.copy[locale];
  const brand=project.product.brand;
  const vertical=height>width;
  const safe=format.safe_area;
  const enter=spring({frame,fps,config:{damping:24,stiffness:130}});
  const recording=project.recordings[locale];
  const fontSize=vertical?64:66;
  const labelStyle: React.CSSProperties={fontSize:fontSize*.31,letterSpacing:2,textTransform:'uppercase',opacity:.65};
  return <AbsoluteFill style={{background:brand.paper,color:brand.ink,fontFamily:"Inter, Arial, 'PingFang TC', sans-serif",paddingTop:safe.top,paddingBottom:safe.bottom,paddingLeft:safe.left,paddingRight:safe.right}}>
    <div style={labelStyle}>{project.product.name}</div>
    {scene.kind==='product' ? <>
      <h1 style={{fontSize:fontSize*.72,lineHeight:1.15,margin:'35px 0 24px',maxWidth:'95%'}}>{copy.headline}</h1>
      <div style={{flex:1,minHeight:0,display:'flex',alignItems:'center',justifyContent:'center',overflow:'hidden',borderRadius:24,background:brand.ink,border:'1px solid '+brand.ink+'22'}}>
        <OffthreadVideo src={staticFile(recording.src)} startFrom={Math.round(((recording.offset_seconds??0)+(scene.source_start_seconds?.[locale]??0))*fps)} muted style={{width:'100%',height:'100%',objectFit:'contain'}}/>
      </div>
      <p style={{fontSize:vertical?27:25,lineHeight:1.4,opacity:.7,marginBottom:0}}>{copy.body}</p>
    </> : <div style={{flex:1,display:'flex',flexDirection:'column',justifyContent:'center',transform:'translateY('+interpolate(enter,[0,1],[35,0])+'px)',opacity:enter}}>
      <div style={{height:8,width:100,background:brand.accent,marginBottom:35}}/>
      <h1 style={{fontSize:vertical?86:100,lineHeight:1.08,letterSpacing:-3,margin:0,overflowWrap:'anywhere'}}>{copy.headline}</h1>
      <p style={{fontSize:vertical?38:40,lineHeight:1.4,maxWidth:vertical?'100%':'80%'}}>{copy.body}</p>
      {scene.kind==='cta' && <p style={{fontSize:vertical?30:34,marginTop:30}}>{project.product.cta_url || project.product.cta}</p>}
    </div>}
  </AbsoluteFill>;
};

const Film: React.FC<Props> = ({project,locale,format}) => <>
  {project.scenes.map((scene: any)=>{
    const [start,end]=times(scene,format);
    return <Sequence key={scene.id} from={Math.round(start*format.fps)} durationInFrames={Math.round((end-start)*format.fps)}><Scene scene={scene} project={project} locale={locale} format={format}/></Sequence>;
  })}
  {project.audio.music && <Audio src={staticFile(project.audio.music)} volume={0.16}/>}
</>;

export const Root = () => <Composition
  id="ProductDemo"
  component={Film}
  width={1080}
  height={1920}
  fps={30}
  durationInFrames={900}
  defaultProps={{project:config,locale:config.locales[0].id,format:config.formats[0]}}
  calculateMetadata={({props})=>({width:props.format.width,height:props.format.height,fps:props.format.fps,durationInFrames:Math.round(props.format.duration_seconds*props.format.fps)})}
/>;
