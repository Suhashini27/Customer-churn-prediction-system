import { NextResponse } from 'next/server';

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { id, action } = body;

        // Dummy payload to simulate calling the real FastAPI score endpoint
        const dummyCustomer = {
            customer_id: id,
            cycle_start: new Date().toISOString(),
            cycle_end: new Date().toISOString(),
            billing_amount: 50,
            last_payment_days_ago: 10,
            plan_tier: "Standard",
            tenure_months: 12,
            monthly_usage_hours: 40,
            active_days: 20,
            login_count: 15,
            avg_session_min: 30,
            device_count: 2,
            add_on_count: 1,
            support_tickets: 0,
            sla_breaches: 0,
            promotions_redeemed: 1,
            email_opens: 5,
            email_clicks: 2,
            last_campaign_days_ago: 15,
            nps_score: 8,
            region: "North America",
            is_autopay: 1,
            is_discounted: 0,
            has_family_bundle: 0
        };

        const res = await fetch('http://127.0.0.1:8000/score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dummyCustomer)
        });

        if (!res.ok) {
            console.warn("FastAPI backend not running or returned error.");
            return NextResponse.json({ success: true, message: `Action '${action}' recorded for ${id} (FastAPI not reachable/errored)` });
        }

        const data = await res.json();
        return NextResponse.json({ success: true, message: `Action '${action}' triggered for ${id}`, score: data });
    } catch (error) {
        return NextResponse.json({ success: false, error: "Failed to process request" }, { status: 500 });
    }
}