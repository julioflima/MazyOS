import { AbsoluteFill, Audio, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';

type Linha = { tipo: 'p' | 'solo' | 'palavra'; texto: string };
type Props = { avatar: string; linhas: Linha[]; audio: string };

// O slide final deixou de ser PNG: os elementos entram um a um, como nas
// outras cenas, em vez de aparecerem todos de uma vez (Julio, 19/09/26).
export const Fecho: React.FC<Props> = ({ avatar, linhas, audio }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const mola = (atraso: number) =>
    spring({ frame: frame - atraso, fps, config: { damping: 200, stiffness: 90 } });

  const entrada = (i: number) => {
    const m = mola(10 + i * 12);
    return { opacity: m, transform: `translateY(${interpolate(m, [0, 1], [30, 0])}px)` };
  };

  const cab = mola(0);

  return (
    <AbsoluteFill style={{ backgroundColor: '#000', fontFamily: 'Inter, system-ui, sans-serif', color: '#FAFAF7' }}>
      <Audio src={staticFile(audio)} />

      <div style={{ position: 'absolute', top: 150, left: 76, display: 'flex', alignItems: 'center', gap: 20,
                    opacity: cab, transform: `translateY(${interpolate(cab, [0, 1], [20, 0])}px)` }}>
        <Img src={staticFile(avatar)} style={{ width: 96, height: 96, borderRadius: '50%', objectFit: 'cover' }} />
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 34, fontWeight: 700 }}>
            Izabel · Multiplic
            <svg width="34" height="34" viewBox="0 0 40 40" fill="rgb(0,149,246)">
              <path fillRule="evenodd" d="M19.998 3.094 14.638 0l-2.972 5.15H5.432v6.354L0 14.64 3.094 20 0 25.359l5.432 3.137v5.905h5.975L14.638 40l5.36-3.094L25.358 40l3.232-5.6h6.162v-6.01L40 25.359 36.905 20 40 14.641l-5.248-3.03v-6.46h-6.419L25.358 0l-5.36 3.094Zm7.415 11.225 2.254 2.287-11.43 11.5-6.835-6.93 2.244-2.258 4.587 4.581 9.18-9.18Z" />
            </svg>
          </div>
          <div style={{ fontSize: 28, color: 'rgba(250,250,247,.55)' }}>@izabelmultiplic</div>
        </div>
      </div>

      <AbsoluteFill style={{ justifyContent: 'center', padding: '0 76px', gap: 46 }}>
        {linhas.map((l, i) =>
          l.tipo === 'palavra' ? (
            <div key={i} style={{ ...entrada(i), alignSelf: 'flex-start', color: '#BB842E',
                                  fontSize: 96, fontWeight: 900, letterSpacing: '-0.03em',
                                  lineHeight: 1, paddingBottom: 18, borderBottom: '5px solid #BB842E' }}>
              {l.texto}
            </div>
          ) : (
            <div key={i} style={{ ...entrada(i),
                                  fontSize: l.tipo === 'solo' ? 54 : 42,
                                  fontWeight: l.tipo === 'solo' ? 700 : 400,
                                  lineHeight: 1.4, letterSpacing: '-0.012em' }}>
              {l.texto}
            </div>
          )
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
