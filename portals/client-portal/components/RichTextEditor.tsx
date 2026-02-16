'use client';

import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Image from '@tiptap/extension-image';
import Link from '@tiptap/extension-link';
import Placeholder from '@tiptap/extension-placeholder';
import TextAlign from '@tiptap/extension-text-align';
import Underline from '@tiptap/extension-underline';
import {
    Bold, Italic, Underline as UnderlineIcon, Strikethrough,
    Code, Heading1, Heading2, Heading3, List, ListOrdered,
    Quote, Undo, Redo, Link2, Image as ImageIcon, AlignLeft,
    AlignCenter, AlignRight, AlignJustify
} from 'lucide-react';

interface RichTextEditorProps {
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
}

export function RichTextEditor({ value, onChange, placeholder = 'Start writing...' }: RichTextEditorProps) {
    const editor = useEditor({
        immediatelyRender: false, // Fix SSR hydration mismatch
        extensions: [
            StarterKit.configure({
                heading: {
                    levels: [1, 2, 3]
                }
            }),
            Image.configure({
                inline: true,
                allowBase64: true
            }),
            Link.configure({
                openOnClick: false,
                HTMLAttributes: {
                    class: 'text-blue-600 underline'
                }
            }),
            Placeholder.configure({
                placeholder
            }),
            TextAlign.configure({
                types: ['heading', 'paragraph']
            }),
            Underline
        ],
        content: value,
        onUpdate: ({ editor }) => {
            onChange(editor.getHTML());
        },
        editorProps: {
            attributes: {
                class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-xl max-w-none focus:outline-none min-h-[300px] p-4'
            }
        }
    });

    if (!editor) {
        return null;
    }

    const addImage = () => {
        const url = window.prompt('Enter image URL:');
        if (url) {
            editor.chain().focus().setImage({ src: url }).run();
        }
    };

    const setLink = () => {
        const previousUrl = editor.getAttributes('link').href;
        const url = window.prompt('Enter URL:', previousUrl);

        if (url === null) {
            return;
        }

        if (url === '') {
            editor.chain().focus().extendMarkRange('link').unsetLink().run();
            return;
        }

        editor.chain().focus().extendMarkRange('link').setLink({ href: url }).run();
    };

    return (
        <div className="border border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden bg-white dark:bg-gray-800">
            {/* Toolbar */}
            <div className="border-b border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 p-2 flex flex-wrap gap-1">
                {/* Text Formatting */}
                <div className="flex gap-1 border-r border-gray-300 dark:border-gray-600 pr-2">
                    <button
                        onClick={() => editor.chain().focus().toggleBold().run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('bold') ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Bold"
                        type="button"
                    >
                        <Bold className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().toggleItalic().run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('italic') ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Italic"
                        type="button"
                    >
                        <Italic className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().toggleUnderline().run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('underline') ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Underline"
                        type="button"
                    >
                        <UnderlineIcon className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().toggleStrike().run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('strike') ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Strikethrough"
                        type="button"
                    >
                        <Strikethrough className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().toggleCode().run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('code') ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Code"
                        type="button"
                    >
                        <Code className="w-4 h-4" />
                    </button>
                </div>

                {/* Headings */}
                <div className="flex gap-1 border-r border-gray-300 dark:border-gray-600 pr-2">
                    <button
                        onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('heading', { level: 1 }) ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Heading 1"
                        type="button"
                    >
                        <Heading1 className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('heading', { level: 2 }) ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Heading 2"
                        type="button"
                    >
                        <Heading2 className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().toggleHeading({ level: 3 }).run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('heading', { level: 3 }) ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Heading 3"
                        type="button"
                    >
                        <Heading3 className="w-4 h-4" />
                    </button>
                </div>

                {/* Lists */}
                <div className="flex gap-1 border-r border-gray-300 dark:border-gray-600 pr-2">
                    <button
                        onClick={() => editor.chain().focus().toggleBulletList().run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('bulletList') ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Bullet List"
                        type="button"
                    >
                        <List className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().toggleOrderedList().run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('orderedList') ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Numbered List"
                        type="button"
                    >
                        <ListOrdered className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().toggleBlockquote().run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('blockquote') ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Quote"
                        type="button"
                    >
                        <Quote className="w-4 h-4" />
                    </button>
                </div>

                {/* Alignment */}
                <div className="flex gap-1 border-r border-gray-300 dark:border-gray-600 pr-2">
                    <button
                        onClick={() => editor.chain().focus().setTextAlign('left').run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive({ textAlign: 'left' }) ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Align Left"
                        type="button"
                    >
                        <AlignLeft className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().setTextAlign('center').run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive({ textAlign: 'center' }) ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Align Center"
                        type="button"
                    >
                        <AlignCenter className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().setTextAlign('right').run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive({ textAlign: 'right' }) ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Align Right"
                        type="button"
                    >
                        <AlignRight className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().setTextAlign('justify').run()}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive({ textAlign: 'justify' }) ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Justify"
                        type="button"
                    >
                        <AlignJustify className="w-4 h-4" />
                    </button>
                </div>

                {/* Insert */}
                <div className="flex gap-1 border-r border-gray-300 dark:border-gray-600 pr-2">
                    <button
                        onClick={setLink}
                        className={`p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${editor.isActive('link') ? 'bg-gray-300 dark:bg-gray-600' : ''
                            }`}
                        title="Add Link"
                        type="button"
                    >
                        <Link2 className="w-4 h-4" />
                    </button>
                    <button
                        onClick={addImage}
                        className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700"
                        title="Add Image"
                        type="button"
                    >
                        <ImageIcon className="w-4 h-4" />
                    </button>
                </div>

                {/* Undo/Redo */}
                <div className="flex gap-1">
                    <button
                        onClick={() => editor.chain().focus().undo().run()}
                        disabled={!editor.can().undo()}
                        className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                        title="Undo"
                        type="button"
                    >
                        <Undo className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => editor.chain().focus().redo().run()}
                        disabled={!editor.can().redo()}
                        className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                        title="Redo"
                        type="button"
                    >
                        <Redo className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* Editor Content */}
            <EditorContent editor={editor} className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white" />
        </div>
    );
}
