import React, { useRef, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { MeshDistortMaterial, Float, Sphere, PerspectiveCamera, Points, PointMaterial } from '@react-three/drei';
import * as THREE from 'three';

const NeuralCore = () => {
    const coreRef = useRef<THREE.Mesh>(null!);
    const shell1Ref = useRef<THREE.Mesh>(null!);
    const shell2Ref = useRef<THREE.Mesh>(null!);

    useFrame((state) => {
        const time = state.clock.getElapsedTime();
        if (coreRef.current) {
            coreRef.current.rotation.y = time * 0.5;
            coreRef.current.rotation.z = time * 0.3;
        }
        if (shell1Ref.current) {
            shell1Ref.current.rotation.x = time * -0.2;
            shell1Ref.current.rotation.y = time * 0.4;
        }
        if (shell2Ref.current) {
            shell2Ref.current.rotation.z = time * 0.1;
            shell2Ref.current.rotation.x = time * -0.3;
        }
    });

    return (
        <group>
            {/* Central Core */}
            <Float speed={3} rotationIntensity={1} floatIntensity={1}>
                <Sphere ref={coreRef} args={[0.7, 64, 64]}>
                    <MeshDistortMaterial
                        color="#00E5FF"
                        emissive="#00E5FF"
                        emissiveIntensity={1}
                        distort={0.4}
                        speed={3}
                        roughness={0}
                        metalness={1}
                    />
                </Sphere>
            </Float>

            {/* Orbital Shell 1 */}
            <Sphere ref={shell1Ref} args={[1.5, 32, 32]}>
                <meshPhongMaterial
                    color="#00E5FF"
                    wireframe
                    transparent
                    opacity={0.15}
                    emissive="#00E5FF"
                    emissiveIntensity={0.2}
                />
            </Sphere>

            {/* Orbital Shell 2 */}
            <Sphere ref={shell2Ref} args={[2.2, 24, 24]}>
                <meshPhongMaterial
                    color="#00E5FF"
                    wireframe
                    transparent
                    opacity={0.05}
                />
            </Sphere>
        </group>
    );
};

const NeuralParticles = () => {
    const pointsRef = useRef<THREE.Points>(null!);
    const count = 500;
    const positions = React.useMemo(() => {
        const pos = new Float32Array(count * 3);
        for (let i = 0; i < count; i++) {
            pos[i * 3] = (Math.random() - 0.5) * 10;
            pos[i * 3 + 1] = (Math.random() - 0.5) * 10;
            pos[i * 3 + 2] = (Math.random() - 0.5) * 10;
        }
        return pos;
    }, []);

    useFrame((state) => {
        pointsRef.current.rotation.y = state.clock.getElapsedTime() * 0.05;
    });

    return (
        <Points ref={pointsRef} positions={positions}>
            <PointMaterial
                transparent
                color="#00E5FF"
                size={0.03}
                sizeAttenuation={true}
                depthWrite={false}
                blending={THREE.AdditiveBlending}
            />
        </Points>
    );
};

const AuthCanvas: React.FC = () => {
    return (
        <div className="absolute inset-0 w-full h-full pointer-events-none opacity-60">
            <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
                <ambientLight intensity={0.4} />
                <pointLight position={[10, 10, 10]} intensity={1.5} color="#00E5FF" />
                <pointLight position={[-10, -10, -10]} intensity={0.5} color="#00E5FF" />
                <spotLight position={[0, 5, 0]} angle={0.3} penumbra={1} intensity={1} color="#ffffff" />

                <Suspense fallback={null}>
                    <NeuralCore />
                    <NeuralParticles />
                </Suspense>
            </Canvas>
        </div>
    );
};

export default AuthCanvas;
