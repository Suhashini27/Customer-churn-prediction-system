import React from 'react';

const WatchlistData = [
  { id: "#USR-8921", p: 82, plan: "Basic", tenure: "4m" },
  { id: "#USR-4432", p: 68, plan: "Premium", tenure: "18m" },
  { id: "#USR-1209", p: 44, plan: "Standard", tenure: "12m" },
  { id: "#USR-9981", p: 91, plan: "Enterprise", tenure: "32m" },
  { id: "#USR-3122", p: 31, plan: "Basic", tenure: "2m" },
  { id: "#USR-0887", p: 55, plan: "Premium", tenure: "21m" },
  { id: "#USR-5541", p: 28, plan: "Standard", tenure: "9m" },
  { id: "#USR-2119", p: 77, plan: "Premium", tenure: "14m" },
];

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-background text-primary font-inter">
      {/* TOP NAV BAR */}
      <nav className="h-[44px] bg-surface border-b border-border flex items-center justify-between px-4">
        <div className="font-bold text-[14px]">Churn Analytics</div>
        <div className="flex space-x-6 text-[13px] text-muted">
          <span className="text-accent border-b-2 border-accent pb-[12px] font-semibold translate-y-[1px]">Overview</span>
          <span>Watchlist</span>
          <span>Segments</span>
          <span>Model Performance</span>
          <span>Settings</span>
        </div>
        <div className="flex items-center space-x-4 text-[13px]">
          <span className="text-muted">Cycle: May 2025</span>
          <button className="px-3 py-1 border border-border rounded text-primary hover:bg-border/50 transition-colors">
            Export Report
          </button>
        </div>
      </nav>

      {/* KPI STRIP */}
      <div className="grid grid-cols-5 gap-4 p-4">
        <div className="bg-surface border border-border rounded p-4 flex flex-col justify-between">
          <div className="text-[10px] uppercase text-muted tracking-wider mb-2">Total Active Customers</div>
          <div className="text-[22px] font-bold text-primary">48,320</div>
          <div className="text-[11px] text-success flex items-center mt-1">
            <span className="mr-1">↑</span> +1.2%
          </div>
        </div>
        <div className="bg-surface border border-border rounded p-4 flex flex-col justify-between">
          <div className="text-[10px] uppercase text-muted tracking-wider mb-2">Predicted to Churn</div>
          <div className="text-[22px] font-bold text-danger">4,210</div>
          <div className="text-[11px] text-danger flex items-center mt-1">
            <span className="mr-1">↑</span> +0.5%
          </div>
        </div>
        <div className="bg-surface border border-border rounded p-4 flex flex-col justify-between">
          <div className="text-[10px] uppercase text-muted tracking-wider mb-2">Churn Rate This Cycle</div>
          <div className="text-[22px] font-bold text-danger">8.7%</div>
          <div className="text-[11px] text-danger flex items-center mt-1">
            <span className="mr-1">↑</span> +0.2%
          </div>
        </div>
        <div className="bg-surface border border-border rounded p-4 flex flex-col justify-between">
          <div className="text-[10px] uppercase text-muted tracking-wider mb-2">Retention Actions Sent</div>
          <div className="text-[22px] font-bold text-accent">3,180</div>
          <div className="text-[11px] text-success flex items-center mt-1">
            <span className="mr-1">↑</span> +15%
          </div>
        </div>
        <div className="bg-surface border border-border rounded p-4 flex flex-col justify-between">
          <div className="text-[10px] uppercase text-muted tracking-wider mb-2">Est. Revenue at Risk</div>
          <div className="text-[22px] font-bold text-warning">$218,400</div>
          <div className="text-[11px] text-danger flex items-center mt-1">
            <span className="mr-1">↑</span> +3.1%
          </div>
        </div>
      </div>

      {/* MAIN 3-COLUMN GRID */}
      <div className="px-4 pb-4 flex gap-4 h-[560px]">
        
        {/* LEFT COLUMN 38% */}
        <div className="w-[38%] bg-surface border border-border rounded p-4 flex flex-col">
          <div className="text-[12px] font-bold text-primary uppercase tracking-wider mb-4">At-Risk Customer Watchlist</div>
          <div className="flex-1 overflow-auto">
            <table className="w-full text-left text-[13px]">
              <thead>
                <tr className="text-muted border-b border-border">
                  <th className="pb-2 font-normal">Customer ID</th>
                  <th className="pb-2 font-normal">Churn Prob</th>
                  <th className="pb-2 font-normal">Plan</th>
                  <th className="pb-2 font-normal">Tenure</th>
                </tr>
              </thead>
              <tbody>
                {WatchlistData.map((row, i) => (
                  <tr key={i} className="border-b border-border last:border-0">
                    <td className="py-3 text-primary">{row.id}</td>
                    <td className="py-3 flex items-center gap-2">
                      <div className="w-16 h-1.5 bg-background rounded overflow-hidden">
                        <div 
                          className={`h-full ${row.p > 50 ? 'bg-danger' : 'bg-warning'}`} 
                          style={{ width: `${row.p}%` }}
                        ></div>
                      </div>
                      <span className="font-bold">{row.p}%</span>
                    </td>
                    <td className="py-3 text-primary">{row.plan}</td>
                    <td className="py-3 text-primary">{row.tenure}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* CENTER COLUMN 36% */}
        <div className="w-[36%] flex flex-col gap-4">
          <div className="bg-surface border border-border rounded p-4 h-1/2">
            <div className="flex justify-between items-center mb-6">
              <div className="text-[12px] font-bold text-primary uppercase tracking-wider">Churn Probability Distribution</div>
            </div>
            <div className="flex justify-between text-[12px] text-primary mb-2">
              <span>0-25% Risk</span>
              <span>12,400</span>
            </div>
            {/* Single stacked bar */}
            <div className="w-full h-8 flex rounded overflow-hidden mb-6">
              <div className="bg-success" style={{ width: '40%' }}></div>
              <div className="bg-warning" style={{ width: '28%' }}></div>
              <div className="bg-alert" style={{ width: '20%' }}></div>
              <div className="bg-danger" style={{ width: '12%' }}></div>
            </div>
            {/* Legend */}
            <div className="flex justify-between text-[11px] text-muted">
              <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-success"></div>Low</div>
              <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-warning"></div>Mid</div>
              <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-alert"></div>High</div>
              <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-danger"></div>Critical</div>
            </div>
          </div>

          <div className="bg-surface border border-border rounded p-4 h-1/2 flex flex-col">
            <div className="text-[12px] font-bold text-primary uppercase tracking-wider mb-6">Churn Rate by Plan Tier</div>
            <div className="flex-1 flex items-end justify-between px-6 pb-2">
              <div className="flex flex-col items-center group">
                <span className="text-[11px] text-primary mb-2">14.2%</span>
                <div className="w-12 bg-accent" style={{ height: '142px' }}></div>
                <span className="text-[11px] text-muted mt-2">Basic</span>
              </div>
              <div className="flex flex-col items-center">
                <span className="text-[11px] text-primary mb-2">9.8%</span>
                <div className="w-12 bg-accent" style={{ height: '98px' }}></div>
                <span className="text-[11px] text-muted mt-2">Standard</span>
              </div>
              <div className="flex flex-col items-center">
                <span className="text-[11px] text-primary mb-2">6.1%</span>
                <div className="w-12 bg-accent" style={{ height: '61px' }}></div>
                <span className="text-[11px] text-muted mt-2">Premium</span>
              </div>
              <div className="flex flex-col items-center">
                <span className="text-[11px] text-primary mb-2">3.4%</span>
                <div className="w-12 bg-accent" style={{ height: '34px' }}></div>
                <span className="text-[11px] text-muted mt-2">Enterprise</span>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN 26% */}
        <div className="w-[26%] bg-surface border border-border rounded flex flex-col">
          <div className="p-4 flex-1">
            <div className="text-[12px] font-bold text-primary uppercase tracking-wider mb-6">Top Churn Drivers</div>
            
            <div className="flex flex-col gap-5">
              <div>
                <div className="flex justify-between items-center mb-1">
                  <span className="font-bold text-[13px] text-primary">Support Ticket Volume</span>
                  <span className="bg-danger/20 text-danger text-[10px] px-1.5 py-0.5 rounded-[2px] font-bold uppercase">High Impact</span>
                </div>
                <div className="text-[11px] text-muted mb-2">+12% increase this period</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-1 bg-background rounded"><div className="h-full bg-danger w-[85%]"></div></div>
                  <span className="text-[11px] text-primary font-bold">0.85</span>
                </div>
              </div>

              <div>
                <div className="flex justify-between items-center mb-1">
                  <span className="font-bold text-[13px] text-primary">Contract Term Length</span>
                  <span className="bg-warning/20 text-warning text-[10px] px-1.5 py-0.5 rounded-[2px] font-bold uppercase">Med Impact</span>
                </div>
                <div className="text-[11px] text-muted mb-2">Month-to-month segment</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-1 bg-background rounded"><div className="h-full bg-warning w-[62%]"></div></div>
                  <span className="text-[11px] text-primary font-bold">0.62</span>
                </div>
              </div>

              <div>
                <div className="flex justify-between items-center mb-1">
                  <span className="font-bold text-[13px] text-primary">Data Usage Drop</span>
                  <span className="bg-danger/20 text-danger text-[10px] px-1.5 py-0.5 rounded-[2px] font-bold uppercase">High Impact</span>
                </div>
                <div className="text-[11px] text-muted mb-2">Below 20th percentile</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-1 bg-background rounded"><div className="h-full bg-danger w-[74%]"></div></div>
                  <span className="text-[11px] text-primary font-bold">0.74</span>
                </div>
              </div>

              <div>
                <div className="flex justify-between items-center mb-1">
                  <span className="font-bold text-[13px] text-primary">Feature Adoption Gap</span>
                  <span className="bg-muted/20 text-muted text-[10px] px-1.5 py-0.5 rounded-[2px] font-bold uppercase">Low Impact</span>
                </div>
                <div className="text-[11px] text-muted mb-2">Core toolkit idle</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-1 bg-background rounded"><div className="h-full bg-muted w-[22%]"></div></div>
                  <span className="text-[11px] text-primary font-bold">0.22</span>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-border p-4">
            <div className="text-[12px] font-bold text-primary uppercase tracking-wider mb-4">Retention Action Summary</div>
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-background rounded p-3 flex flex-col justify-between h-16">
                <span className="text-[11px] text-muted">Email Offers</span>
                <span className="text-[14px] font-bold text-primary">1,240</span>
              </div>
              <div className="bg-background rounded p-3 flex flex-col justify-between h-16">
                <span className="text-[11px] text-muted">Support Calls</span>
                <span className="text-[14px] font-bold text-primary">890</span>
              </div>
              <div className="bg-background rounded p-3 flex flex-col justify-between h-16">
                <span className="text-[11px] text-muted">Payment Nudges</span>
                <span className="text-[14px] font-bold text-primary">620</span>
              </div>
              <div className="bg-background rounded p-3 flex flex-col justify-between h-16">
                <span className="text-[11px] text-muted">Reactivation</span>
                <span className="text-[14px] font-bold text-primary">430</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* BOTTOM ROW - 2 PANELS */}
      <div className="px-4 pb-4 flex gap-4 h-[160px]">
        {/* Left Panel */}
        <div className="w-1/2 bg-surface border border-border rounded p-4 flex flex-col relative overflow-hidden">
          <div className="text-[12px] font-bold text-primary uppercase tracking-wider z-10 mb-2">Historical Churn Trend</div>
          <div className="flex-1 w-full h-full relative z-0 mt-4">
            <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none" className="absolute bottom-0 left-0">
              <defs>
                <linearGradient id="blueGradient" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stopColor="#1F6FEB" stopOpacity="0.3" />
                  <stop offset="100%" stopColor="#1F6FEB" stopOpacity="0" />
                </linearGradient>
              </defs>
              <path d="M0 100 L0 50 Q25 40 50 60 T100 45 L100 100 Z" fill="url(#blueGradient)" />
              <path d="M0 50 Q25 40 50 60 T100 45" fill="none" stroke="#1F6FEB" strokeWidth="2" vectorEffect="non-scaling-stroke" />
            </svg>
          </div>
        </div>

        {/* Right Panel */}
        <div className="w-1/2 bg-surface border border-border rounded p-4 flex flex-col">
          <div className="text-[12px] font-bold text-primary uppercase tracking-wider mb-4">Retention Campaign Analysis</div>
          <div className="grid grid-cols-2 gap-x-6 gap-y-4 flex-1">
            <div className="flex flex-col justify-center">
              <div className="flex justify-between items-center mb-1">
                <span className="text-[11px] text-muted uppercase">Email Offer Success</span>
                <span className="text-[12px] font-bold text-primary">24.5%</span>
              </div>
              <div className="w-full h-1.5 bg-background rounded overflow-hidden">
                <div className="h-full bg-success w-[24.5%]"></div>
              </div>
            </div>
            
            <div className="flex flex-col justify-center">
              <div className="flex justify-between items-center mb-1">
                <span className="text-[11px] text-muted uppercase">Direct Support Call</span>
                <span className="text-[12px] font-bold text-primary">68.2%</span>
              </div>
              <div className="w-full h-1.5 bg-background rounded overflow-hidden">
                <div className="h-full bg-success w-[68.2%]"></div>
              </div>
            </div>
            
            <div className="flex flex-col justify-center">
              <div className="flex justify-between items-center mb-1">
                <span className="text-[11px] text-muted uppercase">Automated Nudges</span>
                <span className="text-[12px] font-bold text-primary">12.1%</span>
              </div>
              <div className="w-full h-1.5 bg-background rounded overflow-hidden">
                <div className="h-full bg-warning w-[12.1%]"></div>
              </div>
            </div>
            
            <div className="flex flex-col justify-center">
              <div className="flex justify-between items-center mb-1">
                <span className="text-[11px] text-muted uppercase">Contract Renewal Credit</span>
                <span className="text-[12px] font-bold text-primary">41.8%</span>
              </div>
              <div className="w-full h-1.5 bg-background rounded overflow-hidden">
                <div className="h-full bg-success w-[41.8%]"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* FOOTER BAR */}
      <footer className="h-10 bg-surface border-t border-border flex items-center justify-between px-4 text-[11px] text-muted">
        <div>Model Version: 4.2.1 (Production) | Last Sync: 14 mins ago</div>
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-success"></div>
          All Systems Operational
        </div>
      </footer>
    </div>
  );
}