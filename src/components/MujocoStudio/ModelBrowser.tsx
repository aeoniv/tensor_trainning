"use client";

import React from "react";
import { Search, Folder, Zap } from "lucide-react";

// Representative list of models from Menagerie for the demo
const MENAGERIE_MODELS = [
    { name: "Unitree G1", path: "/mujoco/menagerie/unitree_g1/scene.xml", icon: "🤖" },
    { name: "Unitree H1", path: "/mujoco/menagerie/unitree_h1/scene.xml", icon: "🧍" },
    { name: "Boston Dynamics Spot", path: "/mujoco/menagerie/boston_dynamics_spot/scene.xml", icon: "🐕" },
    { name: "Agility Cassie", path: "/mujoco/menagerie/agility_cassie/scene.xml", icon: "🦵" },
    { name: "Anybotics ANYmal C", path: "/mujoco/menagerie/anybotics_anymal_c/scene.xml", icon: "🐂" },
    { name: "Franka Emika Panda", path: "/mujoco/menagerie/franka_emika_panda/scene.xml", icon: "🦾" },
    { name: "Universal Robots UR5e", path: "/mujoco/menagerie/universal_robots_ur5e/scene.xml", icon: "🏗️" },
    { name: "Shadow Hand", path: "/mujoco/menagerie/shadow_hand/left_hand.xml", icon: "🖐️" },
    { name: "Aloha", path: "/mujoco/menagerie/aloha/scene.xml", icon: "🦀" },
    { name: "Fly Body", path: "/mujoco/menagerie/flybody/scene.xml", icon: "🪰" },
    { name: "Bitcraze Crazyflie 2", path: "/mujoco/menagerie/bitcraze_crazyflie_2/scene.xml", icon: "🚁" },
];

interface ModelBrowserProps {
    onSelectModel: (path: string) => void;
    currentModel?: string;
}

export default function ModelBrowser({ onSelectModel, currentModel }: ModelBrowserProps) {
    const [searchTerm, setSearchTerm] = React.useState("");

    const filteredModels = MENAGERIE_MODELS.filter(m =>
        m.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="flex flex-col gap-4 w-full max-w-[300px] border-r p-4 bg-card h-full">
            <div className="flex items-center gap-2 pb-4 border-b">
                <Folder className="w-5 h-5 text-primary" />
                <h3 className="font-bold text-lg">Model Explorer</h3>
            </div>

            <div className="relative">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <input
                    placeholder="Search models..."
                    className="w-full pl-8 pr-4 py-2 text-sm rounded-md bg-muted border focus:outline-none focus:ring-1 focus:ring-primary"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>

            <div className="flex-1 overflow-y-auto space-y-1 pr-2 custom-scrollbar">
                {filteredModels.map((model) => (
                    <button
                        key={model.path}
                        onClick={() => onSelectModel(model.path)}
                        className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all text-left ${currentModel === model.path
                                ? "bg-primary text-primary-foreground shadow-md scale-[1.02]"
                                : "hover:bg-muted text-muted-foreground hover:text-foreground"
                            }`}
                    >
                        <span className="text-xl">{model.icon}</span>
                        <div className="flex flex-col">
                            <span className="font-medium">{model.name}</span>
                            <span className="text-[10px] opacity-70 truncate max-w-[180px]">
                                {model.path.split('/').slice(-2).join('/')}
                            </span>
                        </div>
                    </button>
                ))}
            </div>

            <div className="pt-4 border-t">
                <div className="p-3 rounded-lg bg-primary/5 border border-primary/10 flex items-start gap-3">
                    <Zap className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                    <p className="text-[10px] leading-relaxed text-muted-foreground">
                        Select a robot to load its MuJoCo Menagerie scene. Large models may take a few seconds to fetch assets into the browser VFS.
                    </p>
                </div>
            </div>
        </div>
    );
}
