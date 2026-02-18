import { useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "./api/client";
import { Dashboard } from "./dashboard/Dashboard";
import { ClusterView } from "./components/ClusterView";
import { Hero } from "./sections/Hero";
import { WhySection } from "./sections/WhySection";
import { ScenariosSection } from "./sections/ScenariosSection";
import { ArchitectureSection } from "./sections/ArchitectureSection";
import { TechStackSection } from "./sections/TechStackSection";
import { Footer } from "./sections/Footer";

function App() {
  const dashboardRef = useRef<HTMLDivElement>(null);
  const [dashboardScenario, setDashboardScenario] = useState<string | undefined>();

  const { data: stats } = useQuery({
    queryKey: ["stats"],
    queryFn: api.getStats,
  });

  const { data: clusters } = useQuery({
    queryKey: ["clusters"],
    queryFn: api.getClusters,
  });

  const scrollToDashboard = (scenario?: string) => {
    setDashboardScenario(scenario);
    dashboardRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <Hero stats={stats} onTryDemo={() => scrollToDashboard()} />
      <WhySection />
      <ScenariosSection onExplore={scrollToDashboard} />

      <section ref={dashboardRef} className="max-w-7xl mx-auto px-6 py-16">
        <h2 className="text-2xl font-bold mb-6">Live Dashboard</h2>
        <Dashboard initialScenario={dashboardScenario} />
      </section>

      {clusters && clusters.length > 0 && (
        <section className="max-w-6xl mx-auto px-6 py-16">
          <h2 className="text-2xl font-bold mb-6">UX Confusion Clusters</h2>
          <ClusterView clusters={clusters} />
        </section>
      )}

      <ArchitectureSection />
      <TechStackSection />
      <Footer />
    </div>
  );
}

export default App;
