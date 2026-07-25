import type { Tag } from "@/types/TagTypes";
import TagSelector from "./TagSelector";

export interface SortOption<TSort extends string> {
  value: TSort;
  label: string;
}

export interface SearchScope {
  count: number;
  label: string;
}

interface Props<TSort extends string, TagType extends Tag> {
  search: string;
  onSearchChange: (value: string) => void;
  scope: SearchScope;

  showFavorites: boolean;
  onToggleFavorites: () => void;

  sortMethod: TSort;
  onSortChange: (value: TSort) => void;
  sortOptions: SortOption<TSort>[];

  tags?: TagType[];
  selectedTags: number[];
  onTagsChange: (tags: number[]) => void;

  onManageTags?: () => void;
  manageTagsLabel?: string;
}

export default function SearchBar<TSort extends string, TagType extends Tag>({
  search,
  onSearchChange,
  scope,
  showFavorites,
  onToggleFavorites,
  sortMethod,
  onSortChange,
  sortOptions,
  tags,
  selectedTags,
  onTagsChange,
  onManageTags,
  manageTagsLabel = "Tags",
}: Props<TSort, TagType>) {
  const placeholder =
    scope.count <= 1
      ? "Not much to search through..."
      : `Searching ${scope.count} ${scope.label}`;

  return (
    <>
      <div className="row g-2 align-items-center">
        <div className="col-12 col-md">
          <div className="input-group">
            <input
              value={search}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder={placeholder}
              className="form-control"
            />

            <button
              className={`btn ${
                showFavorites ? "btn-primary" : "btn-outline-secondary"
              }`}
              onClick={onToggleFavorites}
              title="Show favorites"
            >
              <i className={showFavorites ? "bi bi-heart-fill" : "bi bi-heart"} />
            </button>
          </div>
        </div>

        <div className="col-12 col-md-auto">
          <select
            value={sortMethod}
            onChange={(e) => onSortChange(e.target.value as TSort)}
            className="form-select"
          >
            {sortOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {tags && (
        <div className="row g-2 align-items-center mt-1">
          {onManageTags && (
            <div className="col-auto">
              <button
                className="btn btn-outline-secondary"
                onClick={onManageTags}
              >
                {manageTagsLabel}
              </button>
            </div>
          )}

          <div className="col overflow-auto">
            <div className="d-flex flex-nowrap gap-2 overflow-auto">
              <TagSelector
                tags={tags}
                selectedTags={selectedTags}
                onChange={onTagsChange}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}