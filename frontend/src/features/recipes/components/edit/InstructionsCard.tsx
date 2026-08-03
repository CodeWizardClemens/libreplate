import { useEffect, useState } from "react";
import { Form } from "react-bootstrap";

import { recipesPartialUpdate } from "@/api/generated";
import type { Recipe } from "@/api/generated/types.gen";

import { useAutoResizeTextarea } from "@/hooks/useAutoResizeTextarea";

type Props = {
  recipe: Recipe;
};

export default function InstructionsCard({ recipe }: Props) {
  const [instructions, setInstructions] = useState(recipe.instructions ?? "");

  const instructionsRef = useAutoResizeTextarea(instructions);

  useEffect(() => {
    setInstructions(recipe.instructions ?? "");
  }, [recipe]);

  const save = () => {
    recipesPartialUpdate({
      path: {
        id: recipe.id,
      },
      body: {
        instructions,
      },
    });
  };

  return (
    <div className="card mb-4">
      <div className="card-body">
        <Form.Group>
          <Form.Label>Instructions (Markdown supported)</Form.Label>
          <Form.Control
            ref={instructionsRef}
            as="textarea"
            rows={1}
            style={{ overflow: "hidden", resize: "none" }}
            value={instructions}
            onChange={(e) => setInstructions(e.target.value)}
            onBlur={save}
          />
        </Form.Group>
      </div>
    </div>
  );
}
