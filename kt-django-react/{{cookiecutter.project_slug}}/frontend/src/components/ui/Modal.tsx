import { useEffect, useRef, type ReactNode } from "react";

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function Modal({ open, onClose, title, children }: ModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open) dialog.showModal();
    else dialog.close();
  }, [open]);

  return (
    <dialog ref={dialogRef} onClose={onClose} className="rounded-lg p-0 shadow-xl backdrop:bg-black/40">
      <article className="min-w-80 p-6">
        <header className="mb-4">
          <h2 className="text-lg font-semibold">{title}</h2>
        </header>
        <section>{children}</section>
      </article>
    </dialog>
  );
}