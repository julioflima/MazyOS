import { AbsoluteFill, Audio, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';

type Palavra = { t: string; ini: number; fim: number; p?: number };
type Props = { img: string; audio: string; palavras: Palavra[]; logo: string; carrossel?: boolean };

export const Cena: React.FC<Props> = ({ img, audio, palavras, logo, carrossel }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  // zoom forte: acompanha o ritmo da fala em vez de só disfarçar foto parada
  const escala = interpolate(frame, [0, durationInFrames], [1, 1.28], { extrapolateRight: 'clamp' });

  // O texto ACUMULA conforme é falado, até formar o bloco — é assim que o
  // Lord compõe. Legenda palavra a palavra foi testada e não é isso.
  const paras: Palavra[][] = [];
  palavras.forEach((w) => {
    const i = w.p ?? 0;
    (paras[i] ??= []).push(w);
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <Audio src={staticFile(audio)} />
      <AbsoluteFill>
        <Img src={staticFile(img)} style={{
          width: '100%', height: '100%',
          objectFit: carrossel ? 'contain' : 'cover',
          transform: carrossel ? undefined : `scale(${escala})`,
        }} />
      </AbsoluteFill>

      {!carrossel && (
        <>
          <AbsoluteFill style={{
            background: 'linear-gradient(to bottom, rgba(0,0,0,.30) 0%, rgba(0,0,0,.18) 26%, rgba(0,0,0,.93) 72%)',
          }} />
          <AbsoluteFill style={{
            justifyContent: 'flex-end', padding: '0 76px 150px',
            fontFamily: 'Inter, system-ui, sans-serif', color: '#FAFAF7',
          }}>
            {paras.map((par, i) => (
              <p key={i} style={{
                margin: i ? '34px 0 0' : 0, fontSize: 46, fontWeight: 500,
                lineHeight: 1.36, letterSpacing: '-0.012em',
              }}>
                {par.map((w, j) => (
                  <span key={j} style={{ opacity: t >= w.ini ? 1 : 0 }}>{w.t}{' '}</span>
                ))}
              </p>
            ))}
          </AbsoluteFill>
        </>
      )}
    </AbsoluteFill>
  );
};
