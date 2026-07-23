import { useState } from "react";

import { Container } from "react-bootstrap";
import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";
import TopNavbar from "./TopNavbar";

export default function AppLayout() {

    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <>

            <TopNavbar
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