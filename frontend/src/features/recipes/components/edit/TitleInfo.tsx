import type { ReactNode } from "react";

import { recipesPartialUpdate } from "@/api/generated";
import type { Recipe } from "@/api/generated/types.gen";

import { useInlineEdit } from "@/features/recipes/hooks/useInlineEdit";

interface Props {
  recipe: Recipe;
}

interface EditableTextProps<T> {
  field: keyof T;
  edit: ReturnType<typeof useInlineEdit>;
  children: ReactNode;
  multiline?: boolean;
}

function EditableText<T>({
  field,
  edit,
  children,
  multiline = false,
}: EditableTextProps<T>) {
  const isEditing = edit.editing === field;

  if (isEditing) {
    return multiline ? (
      <textarea
        ref={edit.inputRef as React.RefObject<HTMLTextAreaElement>}
        className="form-control text-center"
        rows={1}
        value={edit.value}
        onChange={(e) => edit.setValue(e.target.value)}
        onBlur={edit.save}
        onKeyDown={edit.keyDown}
      />
    ) : (
      <input
        ref={edit.inputRef as React.RefObject<HTMLInputElement>}
        className="form-control text-center mb-2 title-edit"
        value={edit.value}
        onChange={(e) => edit.setValue(e.target.value)}
        onBlur={edit.save}
        onKeyDown={edit.keyDown}
      />
    );
  }

  return (
    <span onClick={() => edit.edit(field)} style={{ cursor: "pointer" }}>
      {children}
    </span>
  );
}

export default function TitleInfo({ recipe }: Props) {
  const edit = useInlineEdit(recipe, (field, value) => {
    recipesPartialUpdate({
      path: {
        id: recipe.id,
      },
      body: {
        [field]: value,
      },
    });
  });

  return (
    <div className="text-center">
      <EditableText field="name" edit={edit}>
        <h1 className="display-5 text-break mb-2">{recipe.name}</h1>
      </EditableText>

      <hr className="mt-0" />

      <EditableText field="summary" edit={edit} multiline>
        <p className="text-muted mb-0">{recipe.summary}</p>
      </EditableText>

      <style>
        {`
          .title-edit {
            font-size: 3rem;
            font-weight: 300;
            line-height: 1.2;
          }
        `}
      </style>
    </div>
  );
}
