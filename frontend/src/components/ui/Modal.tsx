import type { ReactNode, CSSProperties } from "react";

interface ModalProps {
  isOpen: boolean;
  title?: ReactNode;
  onClose: () => void;
  children: ReactNode;
  footer?: ReactNode;
  width?: number | string;
}

export default function Modal({
  isOpen,
  title,
  onClose,
  children,
  footer,
  width = 400,
}: ModalProps) {
  if (!isOpen) {
    return null;
  }

  return (
    <div
      onClick={onClose}
      className="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center"
      style={{
        background: "rgba(0,0,0,0.4)",
        zIndex: 1050,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-3 shadow-lg d-flex flex-column p-4"
        style={
          {
            width,
            maxHeight: "80vh",
          } satisfies CSSProperties
        }
      >
        {title && <h2 className="mb-3">{title}</h2>}

        <div className="flex-grow-1 overflow-auto" style={{ minHeight: 0 }}>
          {children}
        </div>

        {footer && <div className="mt-3">{footer}</div>}
      </div>
    </div>
  );
}
