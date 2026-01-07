import React, { useRef, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { MeshDistortMaterial, Float, Icosahedron, PerspectiveCamera, Points, PointMaterial } from '@react-three/drei';
import * as THREE from 'three';

const InceptionCore = () => {
    const coreRef = useRef<THREE.Mesh>(null!);
    const wireRef = useRef<THREE.Mesh>(null!);

    useFrame((state) => {
        const time = state.clock.getElapsedTime();
        if (coreRef.current) {
            coreRef.current.rotation.y = time * 0.2;
            coreRef.current.scale.setScalar(1 + Math.sin(time * 0.5) * 0.1);
        }
        if (wireRef.current) {
            wireRef.current.rotation.y = time * -0.4;
            wireRef.current.rotation.x = time * 0.2;
        }
    });

    return (
        <group>
            {/* Growth Core */}
            <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
                <Icosahedron ref={coreRef} args={[0.6, 1]}>
                    <MeshDistortMaterial
                        color="#00E5FF"
                        emissive="#00E5FF"
                        emissiveIntensity={0.6}
                        distort={0.3}
                        speed={3}
                        roughness={0}
                        metalness={1}
                    />
                </Icosahedron>
            </Float>

            {/* Expanding Network Wireframe */}
            <Icosahedron ref={wireRef} args={[1.8, 1]}>
                <meshBasicMaterial
                    color="#00E5FF"
                    wireframe
                    transparent
                    opacity={0.1}
                />
            </Icosahedron>
        </group>
    );
};

const RegisterCanvas: React.FC = () => {
    return (
        <div className="absolute inset-0 w-full h-full pointer-events-none opacity-50">
            <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={2} color="#00E5FF" />
                <spotLight position={[0, -10, 10]} angle={0.15} penumbra={1} intensity={1} color="#00E5FF" />

                <Suspense fallback={null}>
                    <InceptionCore />
                </Suspense>
            </Canvas>
        </div>
    );
};

export default RegisterCanvas;
