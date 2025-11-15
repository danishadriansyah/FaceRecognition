"""
Path Utilities - Helper untuk manage paths dengan benar

Gunakan utilities ini di semua tutorial dan project files
untuk ensure semua output tetap di folder yang benar.
"""

import os
from datetime import datetime


def get_script_dir():
    """
    Get directory dimana script dijalankan
    
    Returns:
        str: Absolute path ke script directory
    
    Example:
        >>> script_dir = get_script_dir()
        >>> print(script_dir)  # C:/path/to/minggu-X/learning
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_relative_path(*parts):
    """
    Create relative path from script directory
    
    Args:
        *parts: Path components
    
    Returns:
        str: Absolute path
    
    Example:
        >>> path = get_relative_path('output', 'image.jpg')
        >>> # Returns: C:/path/to/minggu-X/learning/output/image.jpg
    """
    return os.path.join(get_script_dir(), *parts)


def ensure_dir(directory):
    """
    Create directory jika belum exist
    
    Args:
        directory (str): Directory path
    
    Returns:
        str: Directory path
    
    Example:
        >>> output_dir = ensure_dir('output')
        >>> # Creates 'output' folder if doesn't exist
    """
    os.makedirs(directory, exist_ok=True)
    return directory


def get_output_path(filename, subfolder='output'):
    """
    Get full path untuk output file
    
    Args:
        filename (str): Nama file
        subfolder (str): Subfolder dalam script dir (default: 'output')
    
    Returns:
        str: Full path untuk output file
    
    Example:
        >>> path = get_output_path('result.jpg')
        >>> # Returns: C:/path/to/minggu-X/learning/output/result.jpg
    """
    output_dir = get_relative_path(subfolder)
    ensure_dir(output_dir)
    return os.path.join(output_dir, filename)


def get_input_path(filename, subfolder='images'):
    """
    Get full path untuk input file
    
    Args:
        filename (str): Nama file
        subfolder (str): Subfolder dalam script dir (default: 'images')
    
    Returns:
        str: Full path untuk input file
    
    Example:
        >>> path = get_input_path('sample.jpg')
        >>> # Returns: C:/path/to/minggu-X/learning/images/sample.jpg
    """
    return get_relative_path(subfolder, filename)


def get_timestamped_filename(prefix='output', extension='jpg'):
    """
    Generate filename dengan timestamp
    
    Args:
        prefix (str): Prefix untuk filename
        extension (str): File extension tanpa dot
    
    Returns:
        str: Filename dengan timestamp
    
    Example:
        >>> filename = get_timestamped_filename('result', 'jpg')
        >>> # Returns: result_20251114_153045.jpg
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'{prefix}_{timestamp}.{extension}'


def get_timestamped_path(prefix='output', extension='jpg', subfolder='output'):
    """
    Get full path dengan timestamped filename
    
    Args:
        prefix (str): Prefix untuk filename
        extension (str): File extension
        subfolder (str): Output subfolder
    
    Returns:
        str: Full path dengan timestamp
    
    Example:
        >>> path = get_timestamped_path('result', 'jpg')
        >>> # Returns: C:/path/to/minggu-X/learning/output/result_20251114_153045.jpg
    """
    filename = get_timestamped_filename(prefix, extension)
    return get_output_path(filename, subfolder)


def cleanup_old_files(directory, days=7, pattern='*'):
    """
    Hapus file yang lebih lama dari X hari
    
    Args:
        directory (str): Directory path
        days (int): Jumlah hari threshold
        pattern (str): File pattern (glob)
    
    Returns:
        int: Jumlah file yang dihapus
    
    Example:
        >>> deleted = cleanup_old_files('output', days=7)
        >>> print(f'Deleted {deleted} old files')
    """
    import time
    import glob
    
    if not os.path.exists(directory):
        return 0
    
    now = time.time()
    cutoff = now - (days * 86400)
    deleted = 0
    
    for filepath in glob.glob(os.path.join(directory, pattern)):
        if os.path.isfile(filepath):
            if os.path.getmtime(filepath) < cutoff:
                try:
                    os.remove(filepath)
                    deleted += 1
                except Exception as e:
                    print(f"Error deleting {filepath}: {e}")
    
    return deleted


def list_files(directory, extension=None):
    """
    List semua file dalam directory
    
    Args:
        directory (str): Directory path
        extension (str): Filter by extension (optional, e.g., '.jpg')
    
    Returns:
        list: List of file paths
    
    Example:
        >>> images = list_files('images', '.jpg')
        >>> for img_path in images:
        ...     print(img_path)
    """
    if not os.path.exists(directory):
        return []
    
    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if extension is None or filename.lower().endswith(extension.lower()):
                files.append(filepath)
    
    return sorted(files)


def get_file_size_mb(filepath):
    """
    Get file size in MB
    
    Args:
        filepath (str): File path
    
    Returns:
        float: File size in megabytes
    
    Example:
        >>> size = get_file_size_mb('output/video.avi')
        >>> print(f'File size: {size:.2f} MB')
    """
    if os.path.exists(filepath):
        return os.path.getsize(filepath) / (1024 * 1024)
    return 0


def get_directory_size_mb(directory):
    """
    Get total size of directory in MB
    
    Args:
        directory (str): Directory path
    
    Returns:
        float: Total size in megabytes
    
    Example:
        >>> size = get_directory_size_mb('dataset')
        >>> print(f'Dataset size: {size:.2f} MB')
    """
    total = 0
    if os.path.exists(directory):
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total += os.path.getsize(filepath)
    
    return total / (1024 * 1024)


# ==================== USAGE EXAMPLES ====================

if __name__ == '__main__':
    print("Path Utilities - Usage Examples\n")
    
    # Example 1: Get script directory
    print("1. Script Directory:")
    print(f"   {get_script_dir()}\n")
    
    # Example 2: Get relative path
    print("2. Relative Path:")
    output_dir = get_relative_path('output')
    print(f"   {output_dir}\n")
    
    # Example 3: Ensure directory exists
    print("3. Ensure Directory:")
    ensure_dir('output')
    print("   ✅ 'output' directory created/verified\n")
    
    # Example 4: Get output path
    print("4. Output Path:")
    output_file = get_output_path('result.jpg')
    print(f"   {output_file}\n")
    
    # Example 5: Get input path
    print("5. Input Path:")
    input_file = get_input_path('sample.jpg')
    print(f"   {input_file}\n")
    
    # Example 6: Timestamped filename
    print("6. Timestamped Filename:")
    filename = get_timestamped_filename('photo', 'jpg')
    print(f"   {filename}\n")
    
    # Example 7: Timestamped path
    print("7. Timestamped Path:")
    path = get_timestamped_path('result', 'jpg')
    print(f"   {path}\n")
    
    # Example 8: List files
    print("8. List Files:")
    ensure_dir('images')
    files = list_files('images', '.jpg')
    print(f"   Found {len(files)} JPG files\n")
    
    print("="*50)
    print("✅ All examples completed!")
    print("="*50)
