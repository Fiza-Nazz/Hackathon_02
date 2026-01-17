'use client';
import React, { useRef, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { MeshDistortMaterial, Float, Octahedron, Torus, PerspectiveCamera, Stars } from '@react-three/drei';
import * as THREE from 'three';

const VaultCore = () => {
    const coreRef = useRef<THREE.Mesh>(null!);
    const torusRef = useRef<THREE.Mesh>(null!);

    useFrame((state) => {
        const time = state.clock.getElapsedTime();
        if (coreRef.current) {
            coreRef.current.rotation.y = time * 0.4;
            coreRef.current.rotation.x = time * 0.2;
        }
        if (torusRef.current) {
            torusRef.current.rotation.z = time * 0.3;
            torusRef.current.rotation.y = time * 0.5;
        }
    });

    return (
        <group>
            {/* Inner Security Core */}
            <Float speed={4} rotationIntensity={1} floatIntensity={1.5}>
                <Octahedron ref={coreRef} args={[0.8, 0]}>
                    <MeshDistortMaterial
                        color="#00E5FF"
                        emissive="#00E5FF"
                        emissiveIntensity={1.2}
                        distort={0.4}
                        speed={2}
                        roughness={0}
                        metalness={1}
                    />
                </Octahedron>
            </Float>

            {/* Shielding Ring */}
            <Torus ref={torusRef} args={[1.5, 0.05, 16, 100]}>
                <meshPhongMaterial
                    color="#00E5FF"
                    emissive="#00E5FF"
                    emissiveIntensity={0.5}
                    transparent
                    opacity={0.3}
                />
            </Torus>
        </group>
    );
};

const LoginCanvas: React.FC = () => {
    return (
        <div className="absolute inset-0 w-full h-full pointer-events-none opacity-50">
            <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1.5} color="#00E5FF" />
                <spotLight position={[-10, 10, 10]} angle={0.15} penumbra={1} intensity={1} color="#00E5FF" />

                <Suspense fallback={null}>
                    <VaultCore />
                    <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
                </Suspense>
            </Canvas>
        </div>
    );
};

export default LoginCanvas;
