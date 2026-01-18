'use client';
import React from 'react';
import { Canvas } from '@react-three/fiber';
import { Grid, PerspectiveCamera } from '@react-three/drei';

const DashboardBackground: React.FC = () => {
    return (
        <div className="fixed inset-0 w-full h-full pointer-events-none opacity-20 -z-10">
            <Canvas>
                <PerspectiveCamera makeDefault position={[0, 2, 5]} fov={50} />
                <ambientLight intensity={0.5} />
                <Grid
                    infiniteGrid
                    fadeDistance={30}
                    fadeStrength={5}
                    sectionSize={1}
                    sectionThickness={1}
                    sectionColor="#00E5FF"
                    cellSize={0.5}
                />
            </Canvas>
        </div>
    );
};

export default DashboardBackground;
