import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

interface Tag {
  id: number;
  name: string;
}

interface Props<T extends Tag> {
  open: boolean;
  onClose: () => void;

  tags: T[];

  createTag: (name: string) => Promise<unknown>;
  deleteTag: (id: number) => Promise<unknown>;

  onChanged?: () => void;
}

export default function TagModal<T extends Tag>({
  open,
  onClose,
  tags,
  createTag,
  deleteTag,
  onChanged,
}: Props<T>) {
  const [newTag, setNewTag] = useState("");

  const createMutation = useMutation({
    mutationFn: (name: string) => createTag(name),

    onSuccess: () => {
      setNewTag("");
      onChanged?.();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => deleteTag(id),

    onSuccess: () => {
      onChanged?.();
    },
  });

  if (!open) {
    return null;
  }

  function handleCreate() {
    const name = newTag.trim();

    if (!name) {
      return;
    }

    createMutation.mutate(name);
  }

  return (
    <>
      <div className="modal-backdrop fade show" onClick={onClose} />

      <div
        className="modal fade show d-block"
        tabIndex={-1}
        role="dialog"
        aria-modal="true"
      >
        <div className="modal-dialog modal-dialog-centered" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Tags</h5>

              <button
                type="button"
                className="btn-close"
                aria-label="Close"
                onClick={onClose}
              />
            </div>

            <div className="modal-body">
              <div className="input-group mb-3">
                <input
                  className="form-control"
                  value={newTag}
                  onChange={(event) => setNewTag(event.target.value)}
                  placeholder="New tag"
                />

                <button
                  className="btn btn-primary"
                  onClick={handleCreate}
                  disabled={createMutation.isPending}
                >
                  Add
                </button>
              </div>

              <div className="list-group">
                {tags.map((tag) => (
                  <div
                    key={tag.id}
                    className="
                      list-group-item
                      d-flex
                      justify-content-between
                      align-items-center
                    "
                  >
                    <span>{tag.name}</span>

                    <button
                      type="button"
                      className="
                        btn
                        btn-outline-danger
                        btn-sm
                      "
                      disabled={deleteMutation.isPending}
                      onClick={() => deleteMutation.mutate(tag.id)}
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={onClose}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
