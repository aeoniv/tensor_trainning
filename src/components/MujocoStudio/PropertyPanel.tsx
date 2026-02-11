"use client";

import React from "react";
import { Info, Settings2, Eye, Activity } from "lucide-react";

interface PropertyPanelProps {
    model: any;
    data: any;
    vizFlags: any;
    setVizFlags: (flags: any) => void;
}

export default function PropertyPanel({ model, data, vizFlags, setVizFlags }: PropertyPanelProps) {
    if (!model) return (
        <div className="flex flex-col gap-4 w-full max-w-[300px] border-l p-4 bg-card h-full justify-center items-center text-muted-foreground italic text-sm">
            <Info className="w-8 h-8 opacity-20 mb-2" />
            Select a model to view properties
        </div>
    );

    const toggleGroup = (group: number) => {
        const newGroups = { ...vizFlags.groups };
        newGroups[group] = !newGroups[group];
        setVizFlags({ ...vizFlags, groups: newGroups });
    };

    return (
        <div className="flex flex-col gap-6 w-full max-w-[300px] border-l p-4 bg-card h-full overflow-y-auto">
            {/* Header */}
            <div className="flex items-center gap-2 pb-2 border-b">
                <Settings2 className="w-5 h-5 text-primary" />
                <h3 className="font-bold text-lg">Properties</h3>
            </div>

            {/* Model Info */}
            <div className="space-y-4">
                <div className="flex flex-col gap-2">
                    <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">Model Statistics</span>
                    <div className="grid grid-cols-2 gap-2">
                        <div className="p-2 rounded bg-muted/50 border text-center">
                            <span className="block text-[10px] text-muted-foreground">Bodies</span>
                            <span className="text-sm font-mono font-bold">{model.nbody}</span>
                        </div>
                        <div className="p-2 rounded bg-muted/50 border text-center">
                            <span className="block text-[10px] text-muted-foreground">Joints</span>
                            <span className="text-sm font-mono font-bold">{model.njnt}</span>
                        </div>
                        <div className="p-2 rounded bg-muted/50 border text-center">
                            <span className="block text-[10px] text-muted-foreground">Geoms</span>
                            <span className="text-sm font-mono font-bold">{model.ngeom}</span>
                        </div>
                        <div className="p-2 rounded bg-muted/50 border text-center">
                            <span className="block text-[10px] text-muted-foreground">DOFs</span>
                            <span className="text-sm font-mono font-bold">{model.nv}</span>
                        </div>
                    </div>
                </div>

                {/* Visualization Toggles */}
                <div className="flex flex-col gap-2">
                    <div className="flex items-center gap-2 mb-1">
                        <Eye className="w-4 h-4 text-primary" />
                        <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">Visualization Groups</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                        {[0, 1, 2, 3, 4, 5].map(group => (
                            <button
                                key={group}
                                onClick={() => toggleGroup(group)}
                                className={`px-2 py-1.5 rounded border text-[10px] font-bold transition-colors ${vizFlags.groups[group] ? "bg-primary/20 text-primary border-primary/30" : "bg-muted text-muted-foreground hover:bg-muted/80"
                                    }`}
                            >
                                Group {group}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Sensors / Actuators (Placeholder) */}
                <div className="flex flex-col gap-2">
                    <div className="flex items-center gap-2 mb-1">
                        <Activity className="w-4 h-4 text-primary" />
                        <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">Active Actuators</span>
                    </div>
                    {model.nu > 0 ? (
                        <div className="space-y-2">
                            <div className="text-[10px] text-muted-foreground italic pb-1">
                                Controlling {model.nu} actuators
                            </div>
                            {/* In a real app, we'd add sliders here */}
                            <div className="p-2 rounded bg-muted/30 border text-[10px] text-center italic text-muted-foreground">
                                Sliders coming soon...
                            </div>
                        </div>
                    ) : (
                        <div className="text-[10px] text-muted-foreground italic">No actuators in this model</div>
                    )}
                </div>
            </div>

            {/* Hint */}
            <div className="mt-auto pt-4 border-t">
                <p className="text-[10px] text-muted-foreground italic leading-relaxed">
                    Most Menagerie models use Group 0 for primary visuals and Group 1-2 for decorative or collision geoms. Toggle groups to inspect the model.
                </p>
            </div>
        </div>
    );
}
