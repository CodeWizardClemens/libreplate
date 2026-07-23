import { useRef } from "react";

import { useRecipePicture, useUploadRecipePicture } from "../api";

interface Props {
  recipeId: number;
}

export default function RecipeCardPicture({ recipeId }: Props) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { data: picture } = useRecipePicture(recipeId);

  const uploadPicture = useUploadRecipePicture();

  function handleEditClick() {
    fileInputRef.current?.click();
  }

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    uploadPicture.mutate({
      recipeId,
      file,
    });

    event.target.value = "";
  }

  return (
    <div
      className="
        position-relative
        flex-shrink-0
      "
      style={{
        width: "160px",
        height: "160px",
      }}
    >
      {picture?.image ? (
        <img
          src={picture.image}
          alt="Recipe"
          className="
            rounded
            w-100
            h-100
            object-fit-cover
          "
        />
      ) : (
        <div
          className="
            bg-light
            rounded
            d-flex
            align-items-center
            justify-content-center
            text-muted
            w-100
            h-100
          "
        >
          No image
        </div>
      )}

      <button
        type="button"
        className="
          btn
          btn-sm
          btn-light
          position-absolute
          top-0
          end-0
          m-2
          shadow-sm
        "
        onClick={handleEditClick}
        title="Change picture"
      >
        <i className="bi bi-pencil" aria-hidden="true" />
      </button>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="d-none"
        onChange={handleFileChange}
      />
    </div>
  );
}
