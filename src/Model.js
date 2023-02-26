import { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import Scene from './Scene';


function Model() {
    return (
        <Canvas camera={{ fov: 30, position: [60, 30, 10] }}>
            <ambientLight />
            <OrbitControls target={[-10, 20, 0]} />
            <Suspense fallback={null} >
                <Scene />
            </Suspense>
        </Canvas>
    );
}

export default Model;