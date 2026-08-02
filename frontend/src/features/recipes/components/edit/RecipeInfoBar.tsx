import { useEffect, useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";

import { recipesPartialUpdate } from "@/api/generated";
import type { Recipe } from "@/api/generated/types.gen";

type Props = {
  recipe?: Recipe;
};

export default function RecipeInfoBar({ recipe }: Props) {
  const [show, setShow] = useState(false);
  const [hovered, setHovered] = useState(false);

  const [portions, setPortions] = useState("0");
  const [cookingTime, setCookingTime] = useState("0");
  const [preppingTime, setPreppingTime] = useState("0");

  const [draftPortions, setDraftPortions] = useState("0");
  const [draftCookingTime, setDraftCookingTime] = useState("0");
  const [draftPreppingTime, setDraftPreppingTime] = useState("0");

  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (!recipe) return;

    setPortions(String(recipe.portions ?? 0));
    setCookingTime(String(recipe.cooking_time ?? 0));
    setPreppingTime(String(recipe.prepping_time ?? 0));
  }, [recipe]);

  const handleOpen = () => {
    setDraftPortions(portions);
    setDraftCookingTime(cookingTime);
    setDraftPreppingTime(preppingTime);
    setShow(true);
  };

  const handleClose = () => {
    setShow(false);
  };

  const handleSave = async () => {
    if (!recipe?.id) return;

    try {
      setIsSaving(true);

      const response = await recipesPartialUpdate({
        path: {
          id: recipe.id,
        },
        body: {
          portions: Number(draftPortions),
          cooking_time: draftCookingTime,
          prepping_time: draftPreppingTime,
        },
      });

      const updatedRecipe = response.data;

      if (updatedRecipe) {
        setPortions(String(updatedRecipe.portions ?? 0));
        setCookingTime(String(updatedRecipe.cooking_time ?? 0));
        setPreppingTime(String(updatedRecipe.prepping_time ?? 0));
      }

      setShow(false);
    } catch (error) {
      console.error("Failed to update recipe", error);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <>
      <div
        className="d-flex justify-content-around align-items-center gap-4 mb-3 text-secondary small border rounded p-2 w-100 bg-light position-relative"
        style={{ cursor: "pointer" }}
        onClick={handleOpen}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        <span>
          <i className="bi bi-people me-1" />
          {portions} {portions === "1" ? "portion" : "portions"}
        </span>

        <span>
          <i className="bi bi-stopwatch me-1" />
          {cookingTime}m cook
        </span>

        <span>
          <i className="bi bi-stopwatch me-1" />
          {preppingTime}m prep
        </span>

        <i
          className="bi bi-pencil position-absolute end-0 me-3"
          style={{
            opacity: hovered ? 1 : 0,
            transition: "opacity 0.2s ease",
          }}
        />
      </div>

      <Modal show={show} onHide={handleClose} centered>
        <Modal.Header closeButton>
          <Modal.Title>Edit Recipe Info</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Portions</Form.Label>
              <Form.Control
                type="number"
                min={1}
                value={draftPortions}
                onChange={(e) => setDraftPortions(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Cooking Time (minutes)</Form.Label>
              <Form.Control
                type="number"
                min={0}
                value={draftCookingTime}
                onChange={(e) => setDraftCookingTime(e.target.value)}
              />
            </Form.Group>

            <Form.Group>
              <Form.Label>Prepping Time (minutes)</Form.Label>
              <Form.Control
                type="number"
                min={0}
                value={draftPreppingTime}
                onChange={(e) => setDraftPreppingTime(e.target.value)}
              />
            </Form.Group>
          </Form>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose} disabled={isSaving}>
            Cancel
          </Button>

          <Button variant="primary" onClick={handleSave} disabled={isSaving}>
            {isSaving ? "Saving..." : "Save"}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
