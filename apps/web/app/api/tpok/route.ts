import { NextResponse } from 'next/server';

export async function GET() {
    const topAtRisk = [
        { id: "#USR-8921", p: 82, plan: "Basic", tenure: "4m", action: "Nudge" },
        { id: "#USR-4432", p: 68, plan: "Premium", tenure: "18m", action: "Call" },
        { id: "#USR-1209", p: 44, plan: "Standard", tenure: "12m", action: "Email" },
        { id: "#USR-9981", p: 91, plan: "Enterprise", tenure: "32m", action: "Meeting" },
        { id: "#USR-3122", p: 31, plan: "Basic", tenure: "2m", action: "Promo" },
        { id: "#USR-0887", p: 55, plan: "Premium", tenure: "21m", action: "Call" },
        { id: "#USR-5541", p: 28, plan: "Standard", tenure: "9m", action: "Email" },
        { id: "#USR-2119", p: 77, plan: "Premium", tenure: "14m", action: "Call" },
    ];
    return NextResponse.json(topAtRisk);
}