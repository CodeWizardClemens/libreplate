import { useRef } from "react";

import { useRecipePicture, useUploadRecipePicture } from "../../api";

interface Props {
  recipeId: number;
  width?: number;
  height?: number;
}

export default function RecipeCardPicture({
  recipeId,
  width,
  height,
}: Props) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { data: picture } = useRecipePicture(recipeId);

  const uploadPicture = useUploadRecipePicture();

  function stopCardClick(event: React.MouseEvent) {
    event.stopPropagation();
  }

  function handleEditClick(
    event: React.MouseEvent<HTMLButtonElement>
  ) {
    event.stopPropagation();
    fileInputRef.current?.click();
  }

  function handleFileChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    event.stopPropagation();

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
        recipe-picture
      "
      onClick={stopCardClick}
      style={{
        width: `${width}px`,
        height: `${height}px`,
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
          recipe-picture-edit
        "
        onClick={handleEditClick}
        title="Change picture"
      >
        <i
          className="bi bi-pencil"
          aria-hidden="true"
        />
      </button>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="d-none"
        onClick={stopCardClick}
        onChange={handleFileChange}
      />

      <style>
        {`
          .recipe-picture-edit {
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.15s ease-in-out;
          }

          .recipe-picture:hover .recipe-picture-edit {
            opacity: 1;
            pointer-events: auto;
          }
        `}
      </style>
    </div>
  );
}