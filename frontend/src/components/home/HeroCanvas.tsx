'use client';
import React, { useRef, Suspense } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Float, MeshDistortMaterial, Environment, ContactShadows, Icosahedron, MeshWobbleMaterial } from '@react-three/drei';
import * as THREE from 'three';

const Crystal = () => {
    const meshRef = useRef<THREE.Mesh>(null!);
    const wireRef = useRef<THREE.Mesh>(null!);
    const ring1Ref = useRef<THREE.Mesh>(null!);
    const ring2Ref = useRef<THREE.Mesh>(null!);
    const { mouse } = useThree();

    useFrame((state) => {
        const time = state.clock.getElapsedTime();
        if (meshRef.current) {
            meshRef.current.rotation.x = THREE.MathUtils.lerp(meshRef.current.rotation.x, mouse.y * 0.5, 0.1);
            meshRef.current.rotation.y = THREE.MathUtils.lerp(meshRef.current.rotation.y, mouse.x * 0.5, 0.1);
            meshRef.current.position.y = Math.sin(time) * 0.2;
        }
        if (wireRef.current) {
            wireRef.current.rotation.x = time * 0.1;
            wireRef.current.rotation.y = time * 0.15;
        }
        if (ring1Ref.current) {
            ring1Ref.current.rotation.z = time * 0.2;
            ring1Ref.current.rotation.x = time * 0.1;
        }
        if (ring2Ref.current) {
            ring2Ref.current.rotation.y = time * 0.3;
            ring2Ref.current.rotation.z = time * 0.2;
        }
    });

    return (
        <group>
            <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
                <Icosahedron ref={meshRef} args={[1, 0]}>
                    <MeshDistortMaterial
                        color="#00E5FF"
                        emissive="#00E5FF"
                        emissiveIntensity={0.8}
                        distort={0.3}
                        speed={2}
                        roughness={0}
                        metalness={1}
                        transparent
                        opacity={0.9}
                    />
                </Icosahedron>
                {/* Holographic Wireframe Layer */}
                <Icosahedron ref={wireRef} args={[1.2, 1]}>
                    <meshBasicMaterial color="#00E5FF" wireframe transparent opacity={0.1} />
                </Icosahedron>

                {/* Professional Orbital Rings */}
                <mesh ref={ring1Ref} rotation={[Math.PI / 2, 0, 0]}>
                    <torusGeometry args={[1.8, 0.01, 16, 100]} />
                    <meshBasicMaterial color="#00E5FF" transparent opacity={0.3} />
                </mesh>
                <mesh ref={ring2Ref} rotation={[0, Math.PI / 4, 0]}>
                    <torusGeometry args={[2.2, 0.005, 16, 100]} />
                    <meshBasicMaterial color="#00E5FF" transparent opacity={0.15} />
                </mesh>
            </Float>
        </group>
    );
};

const HeroCanvas: React.FC = () => {
    return (
        <div className="w-full h-[500px] lg:h-[700px] relative">
            <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
                <ambientLight intensity={0.5} />
                <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1} color="#00E5FF" />
                <pointLight position={[-10, -10, -10]} intensity={1} color="#00E5FF" />

                <Suspense fallback={null}>
                    <Crystal />
                    <Environment preset="night" />
                    <ContactShadows
                        position={[0, -2.5, 0]}
                        opacity={0.4}
                        scale={10}
                        blur={2.5}
                        far={4.5}
                        color="#00E5FF"
                    />
                </Suspense>
            </Canvas>

            {/* Extreme Glow Background */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-electric-blue/5 blur-[120px] rounded-full -z-10 animate-pulse" />
        </div>
    );
};

export default HeroCanvas;
