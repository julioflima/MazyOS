import { Composition } from 'remotion';
import { Capa } from './Capa';
import { Cena } from './Cena';
import { Fecho } from './Fecho';

export const Root: React.FC = () => (
  <>
  <Composition
    id="Fecho"
    component={Fecho as any}
    durationInFrames={150}
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{ avatar:'izabel.png', linhas:[], audio:'a.mp3' }}
    calculateMetadata={({ props }: any) => ({ durationInFrames: Math.round((props.duracao ?? 5) * 30) })}
  />
  <Composition
    id="Cena"
    component={Cena as any}
    durationInFrames={150}
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{ img:'capa.jpg', audio:'fala-capa.mp3', palavras:[], logo:'logo-branco.png' }}
    calculateMetadata={({ props }: any) => ({ durationInFrames: Math.round((props.duracao ?? 5) * 30) })}
  />
  <Composition
    id="Capa"
    component={Capa}
    durationInFrames={150}
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{
      titulo: ['Ninguém junta', 'tudo antes', 'de começar'],
      subtitulo: 'Sobre a distância entre desejar um bem e se organizar para ele',
      capa: 'capa.jpg',
      logo: 'logo-branco.png',
    }}
    calculateMetadata={({ props }) => ({
      durationInFrames: Math.round((props.duracao ?? 5) * 30),
    })}
  />
  </>
);
