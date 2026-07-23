import { useState } from "react";

import { Container } from "react-bootstrap";
import { Outlet, useMatches } from "react-router-dom";

import Sidebar from "./Sidebar";
import TopNavbar from "./TopNavbar";

type RouteHandle = {
    title?: string;
};

export default function AppLayout() {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    const matches = useMatches();

    const title =
        matches
            .map((match) => match.handle as RouteHandle | undefined)
            .find((handle) => handle?.title)
            ?.title ?? "LibrePlate";

    return (
        <>
            <TopNavbar
                title={title}
                onMenuClick={() => setSidebarOpen(true)}
            />

            <Sidebar
                show={sidebarOpen}
                onHide={() => setSidebarOpen(false)}
            />

            <main className="pt-3">
                <Container fluid="lg">
                    <Outlet />
                </Container>
            </main>
        </>
    );
}