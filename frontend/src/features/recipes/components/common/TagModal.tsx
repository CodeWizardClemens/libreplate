import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import type { RecipeTag } from "@/api/generated";

import { recipesTagsCreate, recipesTagsDeleteDestroy } from "@/api/generated";

interface Props {
  open: boolean;
  onClose: () => void;
  tags: RecipeTag[];
}

export default function TagModal({ open, onClose, tags }: Props) {
  const [newTag, setNewTag] = useState("");

  const createTag = useMutation({
    mutationFn: (name: string) =>
      recipesTagsCreate({
        body: {
          name,
        },
      }),
  });

  const deleteTag = useMutation({
    mutationFn: (id: number) =>
      recipesTagsDeleteDestroy({
        path: {
          id,
        },
      }),
  });

  if (!open) {
    return null;
  }

  function handleCreate() {
    const name = newTag.trim();

    if (!name) {
      return;
    }

    createTag.mutate(name, {
      onSuccess() {
        setNewTag("");
      },
    });
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
                  onChange={(e) => setNewTag(e.target.value)}
                  placeholder="New tag"
                />

                <button className="btn btn-primary" onClick={handleCreate}>
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
                      onClick={() => deleteTag.mutate(tag.id)}
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
