import { useEffect, useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";

import { useUpdateRecipe } from "../../api";

type Props = {
  recipe?: any;
};

export default function RecipeInfoBar({ recipe }: Props) {
  const [show, setShow] = useState(false);
  const [hovered, setHovered] = useState(false);

  const [portions, setPortions] = useState(0);
  const [cookingTime, setCookingTime] = useState(0);
  const [preppingTime, setPreppingTime] = useState(0);

  const [draftPortions, setDraftPortions] = useState(0);
  const [draftCookingTime, setDraftCookingTime] = useState(0);
  const [draftPreppingTime, setDraftPreppingTime] = useState(0);

  const updateRecipe = useUpdateRecipe();

  useEffect(() => {
    if (!recipe) return;

    setPortions(recipe.portions ?? 0);
    setCookingTime(recipe.cooking_time ?? 0);
    setPreppingTime(recipe.prepping_time ?? 0);
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
      await updateRecipe.mutateAsync({
        id: recipe.id,
        data: {
          portions: draftPortions,
          cooking_time: draftCookingTime,
          prepping_time: draftPreppingTime,
        },
      });

      setPortions(draftPortions);
      setCookingTime(draftCookingTime);
      setPreppingTime(draftPreppingTime);

      setShow(false);
    } catch (error) {
      console.error("Failed to update recipe", error);
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
        {(portions ?? 0)} {portions === 1 ? "portion" : "portions"}
      </span>

      <span>
        <i className="bi bi-stopwatch me-1" />
        {(cookingTime ?? 0)}m cook
      </span>

      <span>
        <i className="bi bi-stopwatch me-1" />
        {(preppingTime ?? 0)}m prep
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
                onChange={(e) =>
                  setDraftPortions(Number(e.target.value))
                }
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Cooking Time (minutes)</Form.Label>
              <Form.Control
                type="number"
                min={0}
                value={draftCookingTime}
                onChange={(e) =>
                  setDraftCookingTime(Number(e.target.value))
                }
              />
            </Form.Group>

            <Form.Group>
              <Form.Label>Prepping Time (minutes)</Form.Label>
              <Form.Control
                type="number"
                min={0}
                value={draftPreppingTime}
                onChange={(e) =>
                  setDraftPreppingTime(Number(e.target.value))
                }
              />
            </Form.Group>
          </Form>
        </Modal.Body>

        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={handleClose}
            disabled={updateRecipe.isPending}
          >
            Cancel
          </Button>

          <Button
            variant="primary"
            onClick={handleSave}
            disabled={updateRecipe.isPending}
          >
            {updateRecipe.isPending ? "Saving..." : "Save"}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}