import { useState } from "react";

import RecipeList from "./components/recipes/RecipeList";
import TagSelector from "./components/recipes/TagSelector";
import TagModal from "./components/common/TagModal";

import {
  useCopyRecipe,
  useDeleteRecipe,
  useRecipeTags,
  useRecipes,
  useToggleFavorite,
  useTogglePin,
} from "./api";


type SortMethod =
  | "created_at"
  | "updated_at"
  | "name"
  | "last_used_at";



export default function RecipePage() {


  const recipesQuery = useRecipes();
  const tagsQuery = useRecipeTags();


  const deleteRecipe = useDeleteRecipe();

  const toggleFavorite = useToggleFavorite();
  const togglePin = useTogglePin();

  const copyRecipe = useCopyRecipe();



  const [search, setSearch] = useState("");

  const [selectedTags, setSelectedTags] = useState<number[]>([]);

  const [showFavorites, setShowFavorites] = useState(false);

  const [showTagModal, setShowTagModal] = useState(false);

  const [sortMethod, setSortMethod] =
    useState<SortMethod>("created_at");





  if (recipesQuery.isPending) {

    return (
      <div className="container py-3">
        Loading...
      </div>
    );

  }



  if (recipesQuery.isError) {

    return (
      <div className="container py-3">
        Failed to load recipes.
      </div>
    );

  }



  const recipes = recipesQuery.data;





  function toggleTag(tagId: number) {

    setSelectedTags((current) => {

      if (current.includes(tagId)) {

        return current.filter(
          (id) => id !== tagId
        );

      }


      return [
        ...current,
        tagId,
      ];

    });

  }






  const filteredRecipes = recipes

    .filter((recipe) => {


      const searchTerm =
        search.toLowerCase();



      const matchesSearch =
        recipe.name
          .toLowerCase()
          .includes(searchTerm) ||
        recipe.summary
          .toLowerCase()
          .includes(searchTerm);



      const matchesFavorite =
        !showFavorites ||
        recipe.is_favorite;



      const matchesTags =
        selectedTags.length === 0 ||
        selectedTags.every(
          (tagId) =>
            recipe.tags.some(
              (tag) =>
                tag.id === tagId
            )
        );



      return (
        matchesSearch &&
        matchesFavorite &&
        matchesTags
      );


    })

    .sort((a, b) => {


      if (a.is_pinned && !b.is_pinned) {
        return -1;
      }


      if (!a.is_pinned && b.is_pinned) {
        return 1;
      }




      switch (sortMethod) {


        case "name":

          return a.name.localeCompare(
            b.name
          );



        case "created_at":

          return (
            new Date(b.created_at).getTime() -
            new Date(a.created_at).getTime()
          );



        case "updated_at":

          return (
            new Date(b.updated_at).getTime() -
            new Date(a.updated_at).getTime()
          );



        case "last_used_at":


          if (!a.last_used_at) {
            return 1;
          }


          if (!b.last_used_at) {
            return -1;
          }


          return (
            new Date(b.last_used_at).getTime() -
            new Date(a.last_used_at).getTime()
          );



        default:
          return 0;


      }


    });






  return (

    <div className="container py-3">



      <div className="row g-2 align-items-center">



        <div className="col-auto d-none col-md-block">


          <a
            href="#"
            className="btn btn-primary"
            onClick={(e) =>
              e.preventDefault()
            }
          >
            New recipe
          </a>


        </div>





        <div className="col-12 col-md">


          <div className="input-group">



            <input
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
              placeholder="Search recipes..."
              className="form-control"
            />



            <button
              className={`btn ${
                showFavorites
                  ? "btn-primary"
                  : "btn-outline-secondary"
              }`}
              onClick={() =>
                setShowFavorites(
                  !showFavorites
                )
              }
              title="Show favorites"
            >

              <i
                className={
                  showFavorites
                    ? "bi bi-heart-fill"
                    : "bi bi-heart"
                }
              />

            </button>


          </div>


        </div>





        <div className="col-12 col-md-auto">


          <select
            value={sortMethod}
            onChange={(e) =>
              setSortMethod(
                e.target.value as SortMethod
              )
            }
            className="form-select"
          >

            <option value="created_at">
              Created at
            </option>


            <option value="updated_at">
              Updated at
            </option>


            <option value="name">
              Name
            </option>


            <option value="last_used_at">
              Last used at
            </option>


          </select>


        </div>



      </div>






      <div className="row g-2 align-items-center mt-1">



        <div className="col-auto">


          <button
            className="btn btn-outline-secondary"
            onClick={() =>
              setShowTagModal(true)
            }
          >
            Tags
          </button>


        </div>





        <div className="col overflow-auto">


          {tagsQuery.data && (

            <div className="d-flex flex-nowrap gap-2 overflow-auto">


              <TagSelector
                tags={tagsQuery.data}
                selectedTags={selectedTags}
                onChange={setSelectedTags}
              />


            </div>

          )}


        </div>



      </div>






      <div className="mt-2">


        <RecipeList
          recipes={filteredRecipes}

          onDelete={(id) =>
            deleteRecipe.mutate(id)
          }

          onToggleFavorite={(id) =>
            toggleFavorite.mutate(id)
          }

          onTogglePinned={(id) =>
            togglePin.mutate(id)
          }

          onCopy={(id, name) =>
            copyRecipe.mutate({
              id,
              name,
            })
          }
        />


      </div>






      {tagsQuery.data && (

        <TagModal
          open={showTagModal}
          onClose={() =>
            setShowTagModal(false)
          }
          tags={tagsQuery.data}
        />

      )}



    </div>

  );

}