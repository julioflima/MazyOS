import {
  AbsoluteFill, Audio, Img, interpolate, spring,
  staticFile, useCurrentFrame, useVideoConfig,
} from 'remotion';

type Props = {
  titulo: string[];
  subtitulo: string;
  capa: string;
  logo: string;
  audio?: string;
  duracao?: number;
};

export const Capa: React.FC<Props> = ({ titulo, subtitulo, capa, logo, audio }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // zoom lento e contínuo na foto: aqui ele funciona, porque a foto sangra
  // nos 9:16 inteiros e não há texto dentro dela pra cortar
  const escala = interpolate(frame, [0, durationInFrames], [1, 1.3], {
    extrapolateRight: 'clamp',
  });

  // cada linha do título sobe com mola, uma depois da outra
  const linha = (i: number) =>
    spring({ frame: frame - 8 - i * 7, fps, config: { damping: 200, stiffness: 90 } });

  const sub = spring({
    frame: frame - 10 - titulo.length * 7,
    fps,
    config: { damping: 200, stiffness: 90 },
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {audio && <Audio src={staticFile(audio)} />}

      <AbsoluteFill>
        <Img
          src={staticFile(capa)}
          style={{
            width: '100%', height: '100%', objectFit: 'cover',
            transform: `scale(${escala})`, transformOrigin: 'center center',
          }}
        />
      </AbsoluteFill>

      <AbsoluteFill
        style={{
          background:
            'linear-gradient(to bottom, rgba(0,0,0,.35) 0%, rgba(0,0,0,.25) 38%, rgba(0,0,0,.95) 82%)',
        }}
      />

      <AbsoluteFill
        style={{
          justifyContent: 'flex-end', padding: '0 80px 260px',
          fontFamily: 'Inter, system-ui, sans-serif', color: '#FAFAF7',
        }}
      >
        <h1 style={{ margin: 0, fontSize: 96, fontWeight: 900, lineHeight: 1.02,
                     letterSpacing: '-0.035em', textTransform: 'uppercase' }}>
          {titulo.map((t, i) => (
            <div key={i} style={{ overflow: 'hidden' }}>
              <div style={{
                transform: `translateY(${interpolate(linha(i), [0, 1], [110, 0])}px)`,
                opacity: linha(i),
              }}>{t}</div>
            </div>
          ))}
        </h1>

        <div style={{
          marginTop: 34, fontSize: 34, fontWeight: 400, letterSpacing: '-0.01em',
          color: 'rgba(250,250,247,.82)',
          opacity: sub,
          transform: `translateY(${interpolate(sub, [0, 1], [26, 0])}px)`,
        }}>
          {subtitulo} →
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
