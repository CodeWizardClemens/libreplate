import { Button, Container, Navbar } from "react-bootstrap";
import { List } from "react-bootstrap-icons";

interface Props {
    onMenuClick: () => void;
    title: string;
}

export default function TopNavbar({
    onMenuClick,
    title,
}: Props) {
    return (
        <Navbar
            bg="body"
            className="border-bottom sticky-top"
        >
            <Container fluid>

                <div className="d-flex align-items-center">

                    <Button
                        variant="light"
                        className="me-3"
                        onClick={onMenuClick}
                    >
                        <List size={24} />
                    </Button>

                    <img
                        src="/logo.png"
                        height={50}
                        alt="LibrePlate"
                        className="me-3 d-none d-md-block"
                    />

                    <Navbar.Brand>
                        {title}
                    </Navbar.Brand>

                </div>

            </Container>
        </Navbar>
    );
}