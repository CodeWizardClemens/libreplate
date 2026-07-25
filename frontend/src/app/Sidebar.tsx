import { useState } from "react";

import {
    Nav,
    Offcanvas
} from "react-bootstrap";

import { NavLink } from "react-router-dom";

import {
    bottomNavigation,
    mainNavigation
} from "./navigation";

interface Props {
    show: boolean;
    onHide: () => void;
}

export default function Sidebar({
    show,
    onHide,
}: Props) {

    return (
        <Offcanvas
            show={show}
            onHide={onHide}
            placement="start"
        >
            <Offcanvas.Header closeButton>

                <img
                    src="/logo.png"
                    height={48}
                    alt="LibrePlate"
                    className="me-2"
                />

                <Offcanvas.Title>
                    LibrePlate
                </Offcanvas.Title>

            </Offcanvas.Header>

            <Offcanvas.Body className="d-flex flex-column">

                <Nav
                    variant="pills"
                    className="flex-column gap-1 flex-grow-1"
                >
                    {mainNavigation.map((item) => {
                        const Icon = item.icon;

                        return (
                            <Nav.Link
                                as={NavLink}
                                to={item.path}
                                key={item.path}
                                end={item.path === "/"}
                                onClick={onHide}
                            >
                                <Icon className="me-2" />
                                {item.label}
                            </Nav.Link>
                        );
                    })}
                </Nav>

                <Nav
                    variant="pills"
                    className="flex-column gap-1 border-top pt-3"
                >
                    {bottomNavigation.map((item) => {
                        const Icon = item.icon;

                        return (
                            <Nav.Link
                                as={NavLink}
                                to={item.path}
                                key={item.path}
                                onClick={onHide}
                            >
                                <Icon className="me-2" />
                                {item.label}
                            </Nav.Link>
                        );
                    })}
                </Nav>

            </Offcanvas.Body>

        </Offcanvas>
    );
}