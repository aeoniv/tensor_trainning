"use client";

import React, { useState } from "react";
import MujocoRunner from "../MujocoRunner";
import ModelBrowser from "./ModelBrowser";
import PropertyPanel from "./PropertyPanel";
import { LayoutGrid, Maximize2, Minimize2, PanelRightOpen, PanelRightClose } from "lucide-react";

export default function MujocoStudio() {
    const [modelUrl, setModelUrl] = useState<string>("/mujoco/menagerie/unitree_g1/scene.xml");
    const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Default to closed for focus
    const [isPropertyOpen, setIsPropertyOpen] = useState(true);

    // Joint state between Runner and Property Panel
    const [model, setModel] = useState<any>(null);
    const [data, setData] = useState<any>(null);
    const [vizFlags, setVizFlags] = useState({
        groups: { 0: true, 1: true, 2: true, 3: false, 4: false, 5: false }
    });

    const handleModelLoad = (m: any, d: any) => {
        setModel(m);
        setData(d);
    };

    return (
        <div className="flex flex-col w-full h-[850px] bg-background border rounded-xl overflow-hidden shadow-2xl transition-all duration-300">
            {/* Header / Toolbar */}
            <div className="flex items-center justify-between px-6 py-4 border-b bg-card/50 backdrop-blur-sm z-20">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center text-primary-foreground shadow-lg">
                        <LayoutGrid className="w-6 h-6" />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold tracking-tight">Real Robot Studio</h1>
                        <p className="text-xs text-muted-foreground font-medium uppercase tracking-tighter">Hardware-in-the-loop Interface</p>
                    </div>
                </div>

                <div className="flex items-center gap-3">
                    <button
                        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                        className={`p-2 rounded-md transition-all ${isSidebarOpen ? "bg-primary/10 text-primary" : "hover:bg-muted"}`}
                        title={isSidebarOpen ? "Hide Explorer" : "Show Explorer"}
                    >
                        {isSidebarOpen ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
                    </button>
                    <button
                        onClick={() => setIsPropertyOpen(!isPropertyOpen)}
                        className={`p-2 rounded-md transition-all ${isPropertyOpen ? "bg-primary/10 text-primary" : "hover:bg-muted"}`}
                        title={isPropertyOpen ? "Hide Properties" : "Show Properties"}
                    >
                        {isPropertyOpen ? <PanelRightClose className="w-5 h-5" /> : <PanelRightOpen className="w-5 h-5" />}
                    </button>
                </div>
            </div>

            {/* Main Content Area */}
            <div className="flex flex-1 overflow-hidden">
                {/* Explorer Sidebar */}
                {isSidebarOpen && (
                    <div className="w-[300px] flex-shrink-0 animate-in slide-in-from-left duration-300">
                        <ModelBrowser
                            onSelectModel={setModelUrl}
                            currentModel={modelUrl}
                        />
                    </div>
                )}

                {/* Viewport & Dashboard Container */}
                <div className="flex-1 overflow-hidden bg-muted/20 relative flex flex-col">
                    <MujocoRunner
                        modelUrl={modelUrl}
                        vizFlags={vizFlags}
                        onModelLoad={handleModelLoad}
                    />
                </div>

                {/* Property Sidebar */}
                {isPropertyOpen && (
                    <div className="w-[300px] flex-shrink-0 animate-in slide-in-from-right duration-300">
                        <PropertyPanel
                            model={model}
                            data={data}
                            vizFlags={vizFlags}
                            setVizFlags={setVizFlags}
                        />
                    </div>
                )}
            </div>

            {/* Global Footer */}
            <div className="px-6 py-2 border-t bg-muted/30 flex items-center justify-between text-[11px] text-muted-foreground uppercase tracking-widest font-semibold z-20">
                <div className="flex gap-6">
                    <span className="flex items-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                        Engine: WASM v3.x
                    </span>
                    <span>Resources: Menagerie (Google DeepMind)</span>
                </div>
                <div>
                    Ready to Simulate
                </div>
            </div>
        </div>
    );
}
